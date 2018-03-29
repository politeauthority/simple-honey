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

    :param path: The path of the file to load.
    :type path: str
    """
    misc.record_hit()
    # if not path:
    #     redirect('errors/404')
    redirects = redir.query.filter(redir.uri == path).all()
    # if len(redirects) == 0:
    #     redirect('errors/404')
    return str(redirect) + '    ' + str(redirects)

    # return send_file(file_path, mimetype=mimetype)

# End File: simple-honey/app/controllers/redirection.py
