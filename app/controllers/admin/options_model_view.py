"""Option Model View
This is a really generic, flexible model view for the FlaskOriented "Options" model created by @politeauthority.

"""
from flask_admin.form import SecureForm

from app.controllers.admin.base_model_view import BaseModelView
from app.utilities import admin_tools
from app.utilities import common


class OptionModelView(BaseModelView):
    """
    View Class for Options

    """
    can_delete = False
    can_create = False
    page_size = 25
    column_type_formatters = admin_tools.default_column_formatters()
    column_exclude_list = ['ts_created']
    column_list = ['name', 'value', 'ts_updated']
    column_default_sort = ('ts_created', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated']
    on_model_change = common.refresh_cache_file

# End File: simple-honey/app/controllers/admin/options_model_view.py
