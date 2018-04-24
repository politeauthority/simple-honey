"""Formatter - Utilities

"""
import arrow
import urllib
from jinja2 import Markup
import os

from app.models.option import Option


def date(view, value):
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


def uri_to_webrequest_links(view, context, model, p):
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


def webrequest_to_uri_links(view, context, model, p):
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


def webrequest_to_ip_links(view, context, model, p):
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
