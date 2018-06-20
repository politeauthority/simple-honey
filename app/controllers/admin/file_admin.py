"""File Admin
The FlaskAdmin, FileAdmin interface connection which I've found to be excellent!
This allows for file uploads/ renames and deletion.

"""
from flask import redirect
from flask_admin.contrib.fileadmin import FileAdmin

from app.utilities import auth
from app.utilities import common


class FileAdmin(FileAdmin):

    def is_accessible(self):
        """
        FlaskAdmin built in method for checking page accessibility.

        """
        return auth.check()

    def inaccessible_callback(self, name, **kwargs):
        """
        FlaskAdmin built in method is user doesnt have access

        """
        # redirect to login page if user doesn't have access
        return redirect(common.admin_uri(), 403)

# End File: simple-honey/app/controllers/admin/file_admin.py
