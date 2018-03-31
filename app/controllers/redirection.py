"""Redirection - Controller

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
        return redirect(matched_uri.redirect_url, 301)
    # return send_file(file_path, mimetype=mimetype)

# End File: simple-honey/app/controllers/redirection.py
