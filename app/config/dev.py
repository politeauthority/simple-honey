import os

SQLALCHEMY_DATABASE_URI = '%s://%s:%s@%s:%s' % (
    os.environ.get('SH_DB_ENGINE'),
    os.environ.get('SH_DB_USER'),
    os.environ.get('SH_DB_PASS'),
    os.environ.get('SH_DB_HOST'),
    os.environ.get('SH_DB_PORT'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
THREADS_PER_PAGE = 2

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

APP_DATA_PATH = '/data/'
