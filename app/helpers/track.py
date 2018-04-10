"""Track - Helper

"""
from datetime import datetime

from flask import request
from sqlalchemy.orm.exc import NoResultFound

from app.models.web_request import WebRequest
from app.models.uri import Uri
from app.models.known_ip import KnownIp
from app.helpers import misc


def record_hit():
    """
    Records the request.

    """
    uri = _record_uri()
    ip = _record_ip()
    _record_web_request(uri.id, ip.id)


def _record_uri():
    """
    Records the uri as either an update or insert.

    :returns: New or existing Uri
    :rtype: <Uri>
    """
    requested_path = request.environ['PATH_INFO']
    if requested_path in misc.get_uri_map():
        print('')

        print(requested_path)
        print(requested_path)
        print(requested_path)
        print('')
        print('')
        print('')
        print('')
        try:
            uri = Uri.query.filter(Uri.uri == requested_path).one()
            uri.hits = uri.hits + 1
        except NoResultFound:
            # This should be handled better, but happens when a file is requested that exists
            # that is not a registed ui arg
            uri = Uri()
            uri.uri = requested_path
            uri.response__type = 'file'
            uri.hits = 1
        uri.last_hit = datetime.utcnow()

    else:
        uri = Uri()
        uri.uri = requested_path
        uri.hits = 1
    uri.last_hit = datetime.utcnow()
    uri.save()
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
