"""Web Request Model View
Every request that hit's any of the sources Simple-Honey is reording will go through this model.
This model view will try to display that.

"""

from flask_admin.form import SecureForm

from app.controllers.admin.base_model_view import BaseModelView
from app.utilities import formatters
from app.utilities import admin_tools


class WebRequestModelView(BaseModelView):
    """
    View Class for WebRequests

    """
    can_export = True
    can_create = False
    page_size = 25
    column_type_formatters = admin_tools.default_column_formatters()
    column_formatters = {
        'ip.ip': formatters.webrequest_to_ip_links,
        'uri.uri': formatters.webrequest_to_uri_links
    }
    column_searchable_list = ['uri.uri', 'user_agent', 'domain', 'uri.uri']
    column_list = ['ip.ip', 'domain', 'uri.uri', 'user_agent', 'ts_created']
    column_default_sort = ('ts_created', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated', 'requests']

# End File: simple-honey/app/controllers/admin/web_request_model_view.py
