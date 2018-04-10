"""Home - Controller

"""
import os
from flask import Blueprint, request, redirect, send_file, Response

from app.helpers import misc

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
    misc.record_hit()
    uri_map = misc.get_uri_map()
    if requested_path in uri_map:
        req = uri_map[requested_path]
        if req['response_type'] == 'file':
            return draw_file(requested_path), 200
        elif req['response_type'] == 'redirect':
            return redirect_client(req)
    return ''


def draw_file(path):
    file_path = os.path.join(os.environ.get('HOSTED_FILES'), path)
    if not os.path.exists(file_path):
        return redirect('files/404')

    file_name = file_path[:file_path.rfind('/')]
    ext = file_name[file_name.rfind('.') + 1:].lower()

    mimetype = None
    if ext in ['jpg', 'jpeg', 'gif', 'png']:
        mimetype = 'image/%s' % ext

    response = Response()
    response.headers['Content-Type'] = mimetype

    return send_file(file_path, mimetype=mimetype)


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
    misc.record_hit()
    return str(request.remote_addr)


@home.route('robots.txt', methods=['GET', 'POST'])
def robots():
    """
    /robots.txt
    Real simple robotos.txt file for the bots.

    """
    misc.record_hit()
    return """
User-agent: *\n
Disallow: /\n
"""

# End File: simple-honey/app/controllers/home.py
