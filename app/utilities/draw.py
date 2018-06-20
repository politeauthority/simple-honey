"""Render - Utilities
Draws all the different types of responses for Simple Honey

"""
import os

from flask import send_file, redirect, render_template, Response
from jinja2 import Markup
import markdown2

import app


def file(path):
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


def template(template_file, requested_uri):
    """
    Draws any template within app/templates.

    :param template_file: Template file path relative to app/templates.
    :type template_file: str
    :param requested_uri: Uri the client hit on.
    :type requested_uri: str
    :returns: Rendered jinja template, ready for sending to client.
    :rtype: str
    """
    data = _base_template_arguments(requested_uri)

    return render_template(template_file, **data)


def template_image_center(requested_uri):
    """
    Handles the image center template

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    """
    return template('home/image_center.html', requested_uri)


def nothing():
    """
    Renders the most basic "boiler" template, which contains a Google Analytics tracking code if configured to in the
    admin.

    :returns: Basic html5 boiler template.
    :rtype string:
    """
    data = {}
    data['options'] = app.global_content['options']

    return render_template('boiler.html', **data)


def raw_content(requested_uri):
    """
    Renders raw text to the client, like a public key or something pretty basic.

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    :returns: Simple text to display to client.
    :rtype: str
    """
    return str(requested_uri['value'])


def redirect_client(requested_uri):
    """
    Redirects the client to the value of the Uri's meta_value.

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    :returns: Redirection.
    """
    return redirect(requested_uri['value'], 301)


def custom_template(requested_uri):
    """

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    """
    tempalte_path = os.path.join('/data/hosted_files/templates', requested_uri['value'])
    if not os.path.exists(tempalte_path):
        return nothing()
    phile = open(tempalte_path)

    return phile.read()


def markdown(requested_uri):
    """

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    """
    html = ''
    title = ''
    markdown_template = os.path.join('/data/hosted_files', requested_uri['value'])
    if os.path.exists(markdown_template):
        html = markdown2.markdown_path(markdown_template)
    else:
        html = markdown2.markdown(requested_uri['value'])

    if requested_uri['value']:
        title = requested_uri['value']

    data = _base_template_arguments(requested_uri)
    data['title'] = title
    data['markdown'] = Markup(html)
    return render_template('uris/markdown.html', **data)


def _base_template_arguments(requested_uri):
    """
    The minimal dynamic arguments that we will send to almost every template.

    :param requested_uri: The Uri info to be redirected.
    :type requested_uri: dict
    :returns: Global options, and the clients Request information.markdown
    :rtype: dict
    """
    data = {}
    data['options'] = app.global_content['options']
    data['requested'] = requested_uri
    return data

# End File: simple-honey/app/utilities/draw.py
