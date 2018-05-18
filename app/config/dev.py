import os

SQLALCHEMY_DATABASE_URI = '%s://%s:%s@%s:%s' % (
    os.environ.get('SH_DB_ENGINE'),
    os.environ.get('SH_DB_USER'),
    os.environ.get('SH_DB_PASS'),
    os.environ.get('SH_DB_HOST'),
    os.environ.get('SH_DB_PORT'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG_TB_INTERCEPT_REDIRECTS = True
THREADS_PER_PAGE = 2

# Use a secure, unique and absolutely secret key for
# signing the data.
SRF_SESSION_KEY = '2342423423434'
SESSION_TYPE = 'filesystem'
SECRET_KEY = '3453535346767345'


APP_DATA_PATH = '/data/'
SESSION_FILE_DIR = os.path.join(APP_DATA_PATH, 'cache')
