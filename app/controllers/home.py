"""Home - Controller

"""
from flask import Blueprint, request, redirect

import app
from app.utilities import misc
from app.utilities import track

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('', defaults={'path': ''}, methods=['GET', 'POST'])
@home.route('<path:path>', methods=['GET', 'POST'])
@track.record_uri
def index(path):
    """
    /*
    Index

    :param path: url extensions
    :type path: str
    """
    requested_path = '/' + path
    uri_map = app.global_content['uris']

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
@track.record_uri
def ip():
    """
    /ip
    Fire off the requesting entities IP address

    """
    return str(request.remote_addr)


@home.route('robots.txt', methods=['GET', 'POST'])
@track.record_uri
def robots():
    """
    /robots.txt
    Real simple robotos.txt file for the bots.

    """
    return """
User-agent: *\n
Disallow: /\n
"""

# End File: simple-honey/app/controllers/home.py
