"""Common - Utilities

"""
import os
import pickle
import _pickle as cPickle
from flask import request

import app
from app.models.uri import Uri
from app.models.option import Option


def requested_domain():
    """
    Gets the cleaned up domain requested by the client, to compare against records in the uri table.

    :returns: Simplified domain without protical or port requested.
    :rtype: str
    """
    domain = request.url_root.replace('http://', '').replace('https://', '')
    if ':' in domain:
        domain = domain[:domain.find(':')]
    if domain[len(domain) - 1] == '/':
        domain = domain[:len(domain) - 1]

    return domain


def get_uri_map():
    """
    Gets a dictionary of all currently registed uri routes. Available at g['uri_map']
    @todo: Cache a serialized version of this some where in the local files system

    :returns: The url map.
    :rtype: dict
    """

    uris = Uri.query.all()

    the_map = {}
    for uri in uris:
        if uri.domain:
            uri_key = strip_extra_slashes('%s/%s' % (uri.domain, uri.uri))
        else:
            uri_key = uri.uri
        the_map[uri_key] = {
            'uri_id': uri.id,
            'domain': uri.domain,
            'response_type': uri.response_type,
            'value': uri.meta_val
        }

    # Removing this for now.
    # Check the hosted files for any uris, but prefer the registed URIs first
    # philes = _get_file_uris()
    # for phile_uri, phile_info in philes.items():
    #     if phile_uri not in the_map:
    #         the_map[phile_uri] = phile_info

    return the_map


def match_uri(requested_path):
    """
    Searches through the uri_map to find a registered uri, first checking for something specific to the requested
    domain, if not then searches for a global configuration.

    :param requested_path: The request uri made by the client.
    :type requested_path: str
    :returns: The uri drectrives for handling a uri, or None if no match can be found.
    :rtype: dict or None
    """
    uri_map = app.global_content['uris']
    for uri, info in uri_map.items():
        uri_key_with_domain = strip_extra_slashes("%s/%s" % (requested_domain(), requested_path))
        if uri_key_with_domain == uri:
            return info
    for uri, info in uri_map.items():
        if uri == requested_path:
            return info
    return None


def _get_file_uris():
    """
    Grab all non hidden files on the hosted files directory and return 'em.

    :returns: All files from the hosted files area as a uri_map
    :rtype: dict
    """
    hosted_files = os.listdir(os.environ.get('SH_HOSTED_FILE_URL'))
    the_map = {}
    for phile in hosted_files:
        if phile[0] == '.':
            continue
        if phile == '__pycache__':
            continue
        the_map['/%s' % phile] = {
            'uri_id': None,
            'response_type': 'file',
            'value': None,
        }
    return the_map


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


def load_cached(force=False):
    """
    Loads the cache file for options in and uri mapping, if it exists, or it creates it.

    :param forced: Forces a rebuild of the cache file regaurdless of it's existence.
    :type forced: bool
    :returns: The cached data.
    :rtype: dict:
    """
    if force:
        save_serialized_file()
    try:
        pickled_data = open(os.environ.get('SH_CACHE_FILE'), "rb")
    except OSError:
        save_serialized_file()
        pickled_data = open(os.environ.get('SH_CACHE_FILE'), "rb")
    return cPickle.load(pickled_data)


def admin_uri():
    """
    Helper fucntion to get the admin url quickly

    :returns: admin url, redirect or print friendly
    :rtype: string
    """
    return '/' + app.global_content['options']['admin-url'].value


def strip_extra_slashes(thing):
    """
    Removes extra slashes in a uri, this is hacky, hopefully some refactors could make this unneeded.
    @todo: deal with the protical slashes, currently nothing passes the protical to this, but in the future it may.

    :param thing: The uri to clean.
    :type thing: str
    :returns: Cleaned uri.
    :rtype: str
    """
    if thing[0:3] == 'http':
        print('@todo fix this! common line 148')
    return thing.replace('//', '/')

# End File: simple-honey/app/utilities/common.py
