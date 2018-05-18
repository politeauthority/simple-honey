"""Home - Controller

"""
from flask import Blueprint, request

import app
from app.utilities import track
from app.utilities import draw

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('', defaults={'path': ''}, methods=['GET', 'POST'])
@home.route('<path:path>', methods=['GET', 'POST'])
@track.record_before_hit
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
            return draw.draw_file(req['value']), 200
        elif req['response_type'] == 'redirect':
            return draw.redirect_client(req)
        elif req['response_type'] == 'image_center':
            return draw.template_image_center(req)
        elif req['response_type'] == 'raw_content':
            return draw.raw_content(req)
    return draw.nothing()


@home.route('ip', methods=['GET', 'POST'])
@track.record_before_hit
def ip():
    """
    /ip
    Fire off the requesting entities IP address

    """
    return str(request.remote_addr)


@home.route('robots.txt', methods=['GET', 'POST'])
@track.record_before_hit
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
