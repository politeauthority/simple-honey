"""App
Main file for the entire flask app.

"""
import _pickle as cPickle
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.contrib.fixers import ProxyFix

# import flask_restless

app = Flask(__name__)
app.config.from_pyfile('config/dev.py')
db = SQLAlchemy(app)

# Models
# @todo: Make this pep8 by loading the modules earlier in this file, if thats even possible.
from app.models.web_request import WebRequest
from app.models.option import Option
from app.models.known_ip import KnownIp
from app.models.uri import Uri

# Controllers
from app.controllers.home import home as ctrl_home
from app.controllers.files import files as ctrl_files
from app.controllers.admin import WebRequestModelView, OptionModelView, KnownIpInfoView, KnownIpModelView, UriModelView

from app.utilities import misc

app.wsgi_app = ProxyFix(app.wsgi_app)


def register_logging(app):
    """
    Connects the logging to the app.

    :param app: Current Flask application
    :type app: <Flask 'app'> obj
    """
    log_dir = os.path.join(app.config['APP_DATA_PATH'], 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    app_log_file = os.path.join(log_dir, 'scs.log')
    handler = TimedRotatingFileHandler(app_log_file, when='midnight', interval=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


def register_blueprints(app):
    """
    Connect the blueprints to the router.
    @note: If ctrl_home is not last, routing gets wonky!

    :param app: Current Flask application
    :type app: <Flask 'app'> obj
    """
    app.register_blueprint(ctrl_files)
    app.register_blueprint(ctrl_home)


def register_admin(app):
    """
    Starts the admin utility

    :param app: Current Flask application
    :type app: <Flask 'app'> obj
    :returns: Flask Admin with registered controllers
    :rtype: <flask_admin> obj
    """
    admin_url = Option.get('admin-url')
    if admin_url:
        admin_url = admin_url.value
    else:
        admin_url = os.environ.get('SH_ADMIN_URL')
    admin = Admin(
        app,
        url="/%s" % admin_url,
        name='Simple-Honey',
        template_mode='bootstrap3')

    admin.add_view(UriModelView(Uri, db.session, name="Uris"))
    admin.add_view(WebRequestModelView(WebRequest, db.session, name="Web Requests"))
    admin.add_view(KnownIpModelView(KnownIp, db.session, name="Known IPs"))
    admin.add_view(FileAdmin(os.environ.get('SH_HOSTED_FILES'), name='Hosted Files'))
    admin.add_view(OptionModelView(Option, db.session, name='Options'))
    admin.add_view(KnownIpInfoView(endpoint='analytics', name='Analytics'))

    return admin


def register_options():
    """
    Creates the default values for options.

    """
    defaults = {
        'admin-url': os.environ.get('SH_ADMIN_URL'),
        'hosted-file-url': os.environ.get('SH_HOSTED_FILES_URL')
    }
    Option.set_defaults(defaults)


def register_session(app):
    """
    Creates the flask session.

    :param app: Current Flask application
    :type app: <Flask 'app'> obj
    """
    sess = Session()
    sess.init_app(app)
    Session(app)


def load_cached():
    try:
        pickled_data = open(os.environ.get('SH_CACHE_FILE'), "rb")
    except OSError:
        misc.save_serialized_file()
        pickled_data = open(os.environ.get('SH_CACHE_FILE'), "rb")
    return cPickle.load(pickled_data)


db.create_all()
DebugToolbarExtension(app)
register_logging(app)
# register_session(app)
register_blueprints(app)
register_options()
admin = register_admin(app)
global_content = load_cached()
# register_api(app)

app.logger.info('Started App')

# End File: simple-honey/app/__init__.py
