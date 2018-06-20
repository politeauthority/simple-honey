"""Simple Honey Model View
This is the base object to help define simple-honey model objects to make them accessable to the admin.

"""
from flask import redirect
from flask_admin.contrib.sqla import ModelView

from app.utilities import auth
from app.utilities import common


class BaseModelView(ModelView):

    def is_accessible(self):
        """
        FlaskAdmin built in method for checking page accessibility.

        """
        return auth.check()

    def inaccessible_callback(self, name, **kwargs):
        """
        FlaskAdmin built in method is user doesnt have access

        """
        return redirect(common.admin_uri(), 403)
