"""Known Ip Model View

"""
from flask_admin.form import SecureForm

from app.controllers.admin.base_model_view import BaseModelView
from app.utilities import admin_tools


class KnownIpModelView(BaseModelView):
    """
    View Class for KnownIps

    """
    page_size = 25
    column_type_formatters = admin_tools.default_column_formatters()
    column_list = ['ip', 'name', 'last_seen', 'ts_created']
    column_searchable_list = ['ip', 'name', 'last_seen', 'ts_created']
    column_exclude_list = ['ts_updated', 'notes']
    column_default_sort = ('last_seen', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated', 'requests']

# End File: simple-honey/app/controllers/admin/known_ip_model_view.py
