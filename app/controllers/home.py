"""Home - Controller

"""

from flask import Blueprint, request

from app.helpers import misc

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('', defaults={'path': ''}, methods=['GET', 'POST'])
@home.route('<path:path>', methods=['GET', 'POST'])
def index(path):
    """
    /*
    Index

    :param path: url extensions
    :type path: str
    """

    misc.record_hit()
    return str(path)
    return ''


@home.route('ip', methods=['GET', 'POST'])
def ip():
    """
    /ip
    Fire off the requesting entities IP address

    """
    misc.record_hit()
    return str(request.remote_addr)


@home.route('robots.txt', methods=['GET', 'POST'])
def robots():
    """
    /robots.txt
    Real simple robotos.txt file for the bots.

    """
    misc.record_hit()
    return """
User-agent: *\n
Disallow: /\n
"""

# End File: simple-honey/app/controllers/home.py
