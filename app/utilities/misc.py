"""Misc - Utilities

"""

import arrow
from jinja2 import Markup
import os
import urllib

from flask import g, send_file, redirect, Response

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
    if g.get('uri_map'):
        return g.uri_map
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


def date_format(view, value):
    """
    Need to figure out how to get local time here and convert from UTC to that.

    :param view: Admin controller view.
    :type view: FlaskAdminView obj
    :param value: The UTC date to be converted to local time.
    :type value: datetime
    :returns: Converted datetime in pretty format.
    :rtype: str
    """
    utc = arrow.get(value, 'UTC')
    local = utc.to(os.environ.get('TZ'))
    return local.humanize()


def format_uri_to_webrequest_links(view, context, model, p):
    """
    Creats a link which searches on the WebRequest FlaskAdmin page for the Uri

    :param view: Flask Admin view.
    :type view: <UriModelView> obj
    :param context: Flask App Context
    :type context: <Context> obj
    :param model: SQL Alchemy
    :type model: model obj
    :param p: ?
    :type: p: ?
    :returns: Formatted link to a search on WebRequest Flask Admin page
    :rtype: str
    """
    admin_url = Option.get('admin-url')
    args = {
        'search': model.uri
    }
    link_args = urllib.parse.urlencode(args)
    the_link = '<a href="/%s/webrequest?%s">%s</a>' % (
        admin_url.value,
        link_args,
        model.uri)
    return Markup(the_link)


def format_webrequest_to_uri_links(view, context, model, p):
    """
    Creats a link which searches on the WebRequest FlaskAdmin page for the Uri

    :param view: Flask Admin view.
    :type view: <UriModelView> obj
    :param context: Flask App Context
    :type context: <Context> obj
    :param model: SQL Alchemy
    :type model: model obj
    :param p: ?
    :type: p: ?
    :returns: Formatted link to a search on WebRequest Flask Admin page
    :rtype: str
    """
    admin_url = Option.get('admin-url')
    args = {
        'search': model.uri.uri
    }
    link_args = urllib.parse.urlencode(args)
    the_link = '<a href="/%s/uri?%s">%s</a>' % (
        admin_url.value,
        link_args,
        model.uri.uri)
    return Markup(the_link)


def format_webrequest_to_ip_links(view, context, model, p):
    """
    Creats a link which searches on the WebRequest FlaskAdmin page for the Uri

    :param view: Flask Admin view.
    :type view: <UriModelView> obj
    :param context: Flask App Context
    :type context: <Context> obj
    :param model: SQL Alchemy
    :type model: model obj
    :param p: ?
    :type: p: ?
    :returns: Formatted link to a search on WebRequest Flask Admin page
    :rtype: str
    """
    admin_url = Option.get('admin-url')
    args = {
        'search': model.ip.ip
    }
    link_args = urllib.parse.urlencode(args)
    the_link = '<a href="/%s/knownip?%s">%s</a>' % (
        admin_url.value,
        link_args,
        model.ip.ip)
    return Markup(the_link)

# End File: simple-honey/app/utilities/misc.py
