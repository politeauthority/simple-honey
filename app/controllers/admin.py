"""Admin - Controller

"""
from datetime import date

from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask_admin.form import SecureForm
from wtforms import validators

from app.utilities import misc


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: misc.date_format
})


class UriModelView(ModelView):
    """
    View Class for URIs

    """
    page_size = 25
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_list = ['uri', 'name', 'last_hit', 'hits', 'response_type']
    column_formatters = dict(uri=misc.format_uri_to_webrequest_links)
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
        ]
    }
    form_args = {
        'uri': {
            'label': 'Uri',
            'validators': [validators.required()]
        },
    }


class WebRequestModelView(ModelView):
    """
    View Class for WebRequests

    """
    can_export = True
    can_create = False
    page_size = 25
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_formatters = {
        'ip.ip': misc.format_webrequest_to_ip_links,
        'uri.uri': misc.format_webrequest_to_uri_links
    }
    column_searchable_list = ['uri.uri', 'user_agent', 'domain', 'uri.uri']
    column_list = ['ip.ip', 'uri.uri', 'user_agent', 'domain', 'ts_created']
    column_default_sort = ('ts_created', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated', 'requests']


class KnownIpModelView(ModelView):
    """
    View Class for KnownIps

    """
    page_size = 25
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_searchable_list = ['ip', 'name', 'last_seen', 'ts_created']
    column_exclude_list = ['ts_updated', 'notes']
    column_default_sort = ('ts_created', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated']


class OptionModelView(ModelView):
    """
    View Class for Options

    """
    can_delete = False
    can_create = False
    page_size = 25
    column_type_formatters = MY_DEFAULT_FORMATTERS
    column_exclude_list = ['ts_created']
    column_list = ['name', 'value', 'ts_updated']
    column_default_sort = ('ts_updated', True)

    form_base_class = SecureForm
    form_excluded_columns = ['ts_created', 'ts_updated']


# End File: simple-honey/app/controllers/admin.py
