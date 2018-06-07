"""Files - Controller

"""

from flask import Blueprint, redirect, send_file, Response
import os

from app.utilities import track

files = Blueprint('Files', __name__, url_prefix='/files/')


@files.route('', defaults={'path': ''})
@files.route('<path:path>', methods=['GET', 'POST'])
@track.record_before_hit
def index(path):
    """
    /files/*
    Index

    :param path: The path of the file to load.
    :type path: str
    """
    if not path:
        return '', 200
    file_path = os.path.join('/data/hosted_files/', path)
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        return redirect('files/404')

    file_name = file_path[:file_path.rfind('/')]
    ext = file_name[file_name.rfind('.') + 1:].lower()

    mimetype = None
    if ext in ['jpg', 'jpeg', 'gif', 'png']:
        mimetype = 'image/%s' % ext

    response = Response()
    response.headers['Content-Type'] = mimetype

    return send_file(file_path, mimetype=mimetype)


@files.route('404')
@track.record_before_hit
def error_404():
    """
    /files/404/

    """
    return 'Error', 404

# End File: simple-honey/app/controllers/files.py
