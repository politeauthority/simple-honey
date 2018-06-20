"""Admin Auth View
FlaskAdmin specific class to handle authentication portal to admin views.
The class structure here is a generic interface, and primarily relies on the the app/controllers/authenticate.py
for logic on how to authenticate a user.

"""
from flask import redirect
from flask_admin import BaseView, expose

from app.utilities import auth
from app.utilities import common
from app.controllers import authenticate


class AuthView(BaseView):

    @expose('/')
    def logout(self):
        """
        Route logout views to destroy sessions.

        """
        return authenticate.flask_admin_auth()

    def is_accessible(self):
        """
        FlaskAdmin built in method for checking page accessibility.
        Here we hook into Simple-Honey's auth checking functionality.

        """
        return auth.check()

    def inaccessible_callback(self, name, **kwargs):
        """
        FlaskAdmin built in method is user doesnt have access

        """
        # redirect to login page if user doesn't have access
        return redirect(common.admin_uri(), 403)

# End File: simple-honey/app/controllers/admin/auth_view.py
