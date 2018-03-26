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
from app.models.web_request import WebRequest
from flask_admin.contrib.sqla import ModelView

# Controllers
from app.controllers.home import home as ctrl_home
from app.controllers.files import files as ctrl_files
from app.controllers.admin import WebRequestModelView

app.wsgi_app = ProxyFix(app.wsgi_app)


def register_logging(app):
    """
    Connects the logging to the app.

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

    """
    app.register_blueprint(ctrl_files)
    app.register_blueprint(ctrl_home)


def register_admin(app):
    """
    Starts the admin utility

    """
    admin = Admin(
        app,
        url="/%s" % os.environ.get('SH_ADMIN_URL'),
        name='Simple-Honey',
        template_mode='bootstrap3')

    modelview_webrequest = WebRequestModelView(WebRequest, db.session)
    admin.add_view(modelview_webrequest)
    # admin.add_view(MicroBlogModelView(User, db.session))

    admin.add_view(FileAdmin('/data/hosted_files', '/files/', name='Hosted Files'))
    return admin


register_logging(app)
register_blueprints(app)
admin = register_admin(app)
db.create_all()
# register_api(app)

app.logger.info('Started App')

# End File: simple-honey/app/__init__.py
