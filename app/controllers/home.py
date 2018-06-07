"""Home - Controller

"""
from flask import Blueprint, request

from app.utilities import track
from app.utilities import draw
from app.utilities import common

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('', defaults={'path': ''}, methods=['GET', 'POST'])
@home.route('<path:path>', methods=['GET', 'POST'])
@track.record_before_hit
def index(path):
    """
    /*
    Index
    This is the main routing method for Simple-Honey. We load up the cached app uris and send the client to where they
    need to go.

    :param path: url extensions
    :type path: str
    """
    requested_path = '/' + path
    matched_uri_path = common.match_uri(requested_path)
    if matched_uri_path:
        if matched_uri_path['response_type'] == 'file':
            return draw.file(matched_uri_path['value'])
        elif matched_uri_path['response_type'] == 'redirect':
            return draw.redirect_client(matched_uri_path), 301
        elif matched_uri_path['response_type'] == 'image_center':
            return draw.template_image_center(matched_uri_path)
        elif matched_uri_path['response_type'] == 'raw_content':
            return draw.raw_content(matched_uri_path)
        elif matched_uri_path['response_type'] == 'custom_template':
            return draw.custom_template(matched_uri_path)
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
