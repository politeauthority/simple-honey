"""Track - utilities
This tool stores the hit from the client in all the appropriate places.
@todo: Add JSON logging here probably.

"""
from datetime import datetime
from functools import wraps

from flask import request
from sqlalchemy.orm.exc import NoResultFound

from app.models.web_request import WebRequest
from app.models.uri import Uri
from app.models.known_ip import KnownIp
from app.utilities import common


def record_hit():
    """
    Records the request.

    """
    uri = _record_uri()
    ip = _record_ip()
    _record_web_request(uri.id, ip.id)


def record_before_hit(f):
    """
    Decorator for recording hits on uris

    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        record_hit()
        return f(*args, **kwargs)
    return decorated_function


def _record_uri():
    """
    Records the uri as either an update or insert.

    :returns: New or existing Uri
    :rtype: <Uri>
    """
    requested_path = request.environ['PATH_INFO']
    if requested_path in common.get_uri_map():
        uri = _get_the_uri_record(requested_path)
        uri.last_hit = datetime.utcnow()
    else:
        uri = Uri()
        uri.uri = requested_path
    if uri.hits:
        uri.hits = uri.hits + 1
    else:
        uri.hits = 1
    uri.last_hit = datetime.utcnow()
    uri.save()
    return uri


def _get_the_uri_record(requested_path):
    """
    Checks the system to see if the client requested URI is registed in the system, based on the uri and domain.

    :param requested_path: The path the client requested.
    :type requested_path: str
    :returns: A Uri representing the request.
    :rtype: <Uri> object
    """
    try:
        uris = Uri.query.filter(Uri.uri == requested_path).all()
        if len(uris) > 1:
            for t_uri in uris:
                if t_uri.domain == common.requested_domain():
                    uri = t_uri
                    return uri
            uri = _create_unregistered_uri(requested_path)
        else:
            uri = uris[0]
    except NoResultFound:
        # This should be handled better, but happens when a file is requested that exists
        # that is not a registed ui arg
        uri = _create_unregistered_uri(requested_path)
    return uri


def _create_unregistered_uri(requested_path):
    """
    Creates a URI if the uri is not currently known to Simple-Honey.

    :param requested_path: The path the client requested.
    :type requested_path: str
    """
    uri = Uri()
    uri.uri = requested_path
    uri.response_type = 'non-mapped-uri'
    uri.domain = common.requested_domain()

    return uri


def _record_ip():
    """
    Saves the clients IP and or udpates last vist.

    :returns: New or existing KnownIp
    :rtype: <KnownIP>
    """
    try:
        known_ip = KnownIp.query.filter(KnownIp.ip == request.remote_addr).one()
    except NoResultFound:
        known_ip = KnownIp()
        known_ip.ip = request.remote_addr
    known_ip.last_seen = datetime.utcnow()
    known_ip.save()
    return known_ip


def _record_web_request(uri_id, ip_id):
    """
    Saves the web request.

    :param uri_id: The Uri's id
    :type url_id: int
    :param ip_id: The IP's id
    :type ip_id: int
    """
    if request.method == 'POST':
        data = request.form['POST']
        request_type = 'POST'
    else:
        data = request.args
        request_type = 'GET'
    wr = WebRequest()
    wr.data = data
    wr.domain = request.url_root
    wr.request_type = request_type
    wr.platform = request.user_agent.platform
    wr.browser_name = request.user_agent.browser
    wr.browser_version = request.user_agent.version
    wr.browser_language = request.user_agent.language
    wr.user_agent = request.user_agent.string
    wr.uri_id = uri_id
    wr.ip_id = ip_id
    wr.save()


# End File: simple-honey/app/helpers/track.py
