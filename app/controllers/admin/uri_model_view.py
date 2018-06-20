"""URI Model View
Admin view controller to display all registered and non registed uris in the Simple-Honey system.

"""
from flask_admin.form import SecureForm
from wtforms import validators

from app.controllers.admin.base_model_view import BaseModelView
from app.utilities import formatters
from app.utilities import admin_tools


class UriModelView(BaseModelView):
    """
    View Class for URIs

    """
    page_size = 25
    column_type_formatters = admin_tools.default_column_formatters()
    column_list = ['domain', 'uri', 'name', 'last_hit', 'hits', 'response_type']
    column_formatters = dict(uri=formatters.uri_to_webrequest_links)
    column_searchable_list = ['uri', 'name']
    column_exclude_list = ['ts_updated']
    column_default_sort = ('ts_updated', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated', 'last_hit', 'requests']
    form_choices = {
        'response_type': [
            ('', 'Blank Response'),
            ('file', 'Static file'),
            ('redirect', 'Redirect'),
            ('image_center', 'Image Centered'),
            ('raw_content', 'Raw Content'),
            ('custom_template', 'Custom Template'),
        ]
    }
    form_args = {
        'uri': {
            'label': 'Uri',
            'validators': [validators.required()]
        },
    }
    on_model_change = admin_tools.refresh_cache_file

# End File: simple-honey/app/controllers/admin/uri_model_view.py
