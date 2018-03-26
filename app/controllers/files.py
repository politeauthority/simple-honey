"""Files - Controller

"""

from flask import Blueprint, redirect, send_file
import os

from app.helpers import misc

files = Blueprint('Files', __name__, url_prefix='/files/')


@files.route('', defaults={'path': ''})
@files.route('<path:path>', methods=['GET', 'POST'])
def index(path):
    """
    /files/*
    Index

    :param path: The path of the file to load.
    :type path: str
    """
    misc.record_hit()
    file_path = os.path.join('/data/hosted_files/', path)
    if not os.path.exists(file_path):
        return redirect('files/404')
    return send_file(
        os.path.join('/data/hosted_files/', path),
        attachment_filename=path[:path.rfind('/')])


@files.route('404')
def error_404():
    """
    /files/404/

    """
    return 'Error', 404

# End File: simple-honey/app/controllers/files.py
