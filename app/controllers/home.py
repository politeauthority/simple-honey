"""Home - Controller

"""
from flask import Blueprint, request, redirect

from app.utilities import misc
from app.utilities import track

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('', defaults={'path': ''}, methods=['GET', 'POST'])
@home.route('<path:path>', methods=['GET', 'POST'])
def index(path):
    """
    /*
    Index

    :param path: url extensions
    :type path: str
    """
    requested_path = '/' + path
    track.record_hit()
    uri_map = misc.get_uri_map()

    if requested_path in uri_map:
        req = uri_map[requested_path]
        if req['response_type'] == 'file':
            return misc.draw_file(req['value']), 200
        elif req['response_type'] == 'redirect':
            return redirect_client(req)
    return ''


def redirect_client(requested_uri):
    """
    Redirects the client to the value of the Uri's meta_value.

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    :returns: Redirection.
    """
    return redirect(requested_uri['value'], 301)


@home.route('ip', methods=['GET', 'POST'])
def ip():
    """
    /ip
    Fire off the requesting entities IP address

    """
    track.record_hit()
    return str(request.remote_addr)


@home.route('robots.txt', methods=['GET', 'POST'])
def robots():
    """
    /robots.txt
    Real simple robotos.txt file for the bots.

    """
    track.record_hit()
    return """
User-agent: *\n
Disallow: /\n
"""

# End File: simple-honey/app/controllers/home.py
