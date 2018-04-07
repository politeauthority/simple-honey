"""App
Main file for the entire flask app.

"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from werkzeug.contrib.fixers import ProxyFix

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin

# import flask_restless

app = Flask(__name__)
app.config.from_pyfile('config/dev.py')
db = SQLAlchemy(app)

# Models
# @todo: Make this pep8 by loading the modules earlier in this file, if thats even possible.
from app.models.web_request import WebRequest
from app.models.option import Option
from app.models.redirection import Redirection
from app.models.known_ip import KnownIp
from app.models.uri import Uri

# Controllers
from app.controllers.home import home as ctrl_home
from app.controllers.files import files as ctrl_files
from app.controllers.redirection import redirection as ctrl_redirection
from app.controllers.admin import WebRequestModelView, OptionModelView, RedirectionModelView, KnownIpModelView

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
    app.register_blueprint(ctrl_redirection)
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

    admin.add_view(WebRequestModelView(WebRequest, db.session))
    admin.add_view(RedirectionModelView(Redirection, db.session))
    admin.add_view(KnownIpModelView(KnownIp, db.session))
    admin.add_view(FileAdmin('/data/hosted_files', '/files/', name='Hosted Files'))
    admin.add_view(OptionModelView(Option, db.session))

    return admin


def register_options():
    """
    Creates the default values for options.

    """
    defaults = {
        'admin-url': os.environ.get('SH_ADMIN_URL')
    }
    Option.set_defaults(defaults)


db.create_all()

register_logging(app)
register_blueprints(app)
register_options()
admin = register_admin(app)
# register_api(app)

app.logger.info('Started App')

# End File: simple-honey/app/__init__.py
