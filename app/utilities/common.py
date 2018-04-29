"""Common - Utilities

"""
import os
import pickle

from flask import send_file, redirect, Response

import app
from app.models.uri import Uri
from app.models.option import Option


def get_uri_map():
    """
    Gets a dictionary of all currently registed uri routes. Available at g['uri_map']
    @todo: Cache a serialized version of this some where in the local files system

    :returns: The url map.
    :rtype: dict
    """
    the_map = {}

    # Check all registed Uris
    uris = Uri.query.all()

    for uri in uris:
        the_map[uri.uri] = {
            'uri_id': uri.id,
            'response_type': uri.response_type,
            'value': uri.meta_val
        }

    # Check the hosted files for any uris, but prefer the registed URIs first
    philes = _get_file_uris()
    for phile_uri, phile_info in philes.items():
        if phile_uri not in the_map:
            the_map[phile_uri] = phile_info

    return the_map


def _get_file_uris():
    """
    Grab all files on the hosted files directory and return.

    :returns: All files from the hosted files area as a uri_map
    :rtype: dict
    """
    hosted_files = os.listdir(os.environ.get('SH_HOSTED_FILE_URL'))
    the_map = {}
    for phile in hosted_files:
        if phile[0] == '.':
            continue
        the_map['/%s' % phile] = {
            'uri_id': None,
            'response_type': 'file',
            'value': None,
        }
    return the_map


def draw_file(path):
    """
    Draws a file from the hosted files directory.

    :param path: The path of the file local to the hosted files directory.
    :type: path: str
    :returns: File contents or redirect
    """
    file_path = os.path.join(os.environ.get('SH_HOSTED_FILES'), path)
    if not os.path.exists(file_path):
        return redirect('/404')

    file_name = file_path[:file_path.rfind('/')]
    ext = file_name[file_name.rfind('.') + 1:].lower()

    mimetype = None
    if ext in ['jpg', 'jpeg', 'gif', 'png', 'pdf']:
        mimetype = 'image/%s' % ext

    response = Response()
    response.headers['Content-Type'] = mimetype

    return send_file(file_path, mimetype=mimetype)


def save_serialized_file():
    """
    Saves options and uri map as a serialized cache file.

    """
    options = Option.load_all()
    data = {
        'options': options,
        'uris': get_uri_map()
    }
    with open(os.environ.get('SH_CACHE_FILE'), 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def admin_uri():
    """
    Helper fucntion to get the admin url quickly

    :returns: admin url, redirect or print friendly
    :rtype: string
    """
    return '/' + app.global_content['options']['admin-url'].value

# End File: simple-honey/app/utilities/common.py
