"""Redirection - Controller
This module works like a URL shorterner with logging. New redirections are setup in the admin and records can be viewed
in the same place as all other hits.

"""

from flask import Blueprint, redirect

from app.models.redirection import Redirection as redir
from app.helpers import misc

redirection = Blueprint('Redirection', __name__, url_prefix='/r/')


@redirection.route('', defaults={'path': ''})
@redirection.route('<path:path>', methods=['GET', 'POST'])
def index(path):
    """
    /r/*
    Index

    :param path: The uri of the redirect
    :type path: str
    """
    misc.record_hit()

    matched_uri = redir.query.filter(redir.uri == path).one()
    if matched_uri:
        if matched_uri.hits:
            matched_uri.hits = matched_uri.hits + 1
        else:
            matched_uri.hits = 1
        matched_uri.save()
        return redirect(matched_uri.redirect_url, 301)
    redirect('errors/404', 404)

# End File: simple-honey/app/controllers/redirection.py
