"""Auth - Utility
Simple module to handle user authentication.

"""

from flask import session
from werkzeug.security import check_password_hash

import app


def login(username, password):
    """
    Checks the user against the stored option objecs for user name and password.

    :param username: The user name
    :type username: str
    :param: password: The plaintext password, not yet hashed.
    :type password: string
    :returns: Success or failure of login opperation
    :rtype: bool
    """
    if (
            app.global_content['options']['admin-user'].value == username and
            check_password_hash(app.global_content['options']['admin-pass'].value, password)):
        session['authenticated'] = True
        session['user'] = username
        return True
    return False


def check():
    """
    Checks if a user has an already authenticaed session

    :returns: Weather or not user is authenticated.
    :rtype: bool
    """
    if session.get('authenticated'):
        return True
    return False

# End File: simple-honey/app/utilities/auth.py
