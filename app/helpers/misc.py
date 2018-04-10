"""Misc - Helpers

"""

import arrow
import os

from flask import g

from app.models.uri import Uri


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
    Grab all files on the hosted files directory and return

    :returns: All
    """
    hosted_files = os.listdir(os.environ.get('HOSTED_FILES'))
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
    # return local.strftime('%b %d %Y %H:%M:%S')

# End File: simple-honey/app/helpers/misc.py
