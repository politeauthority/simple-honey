"""Home - Controller

"""
from flask import Blueprint, request, redirect, render_template

import app
from app.utilities import common
from app.utilities import track

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
            return common.draw_file(req['value']), 200
        elif req['response_type'] == 'redirect':
            return redirect_client(req)
        elif req['response_type'] == 'image_center':
            return template_image_center(req)
        elif req['response_type'] == 'raw_content':
            return draw_raw_content(req)
    return draw_nothing()


def redirect_client(requested_uri):
    """
    Redirects the client to the value of the Uri's meta_value.

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    :returns: Redirection.
    """
    return redirect(requested_uri['value'], 301)


def draw_nothing():
    data = {}
    data['options'] = app.global_content['options']
    return render_template('boiler.html', **data)


def template_image_center(requested_uri):
    """
    Handles the image center template

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    """
    return draw_template('home/image_center.html', requested_uri)


def draw_template(template_file, requested_uri):
    data = {}
    data['options'] = app.global_content['options']
    data['requested'] = requested_uri
    return render_template(template_file, **data)

def draw_raw_content(requested_uri):
    """

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    """
    return str(requested_uri['value'])


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
