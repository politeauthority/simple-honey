"""Admin - Controller

"""
from datetime import date

from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask_admin.form import SecureForm

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
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    page_size = 25
    column_list = ['uri', 'name', 'last_hit', 'hits']
    column_formatters = dict(uri=misc.format_uri_to_webrequest_links)
    column_searchable_list = ['ts_created', 'uri', 'name']
    form_excluded_columns = ['ts_created', 'ts_updated', 'last_hit', 'web_request.requests']
    column_exclude_list = ['ts_updated']
    column_default_sort = ('ts_updated', True)


class WebRequestModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_export = True
    can_create = False
    page_size = 25
    column_formatters = {
        'ip.ip': misc.format_webrequest_to_ip_links,
        'uri.uri': misc.format_webrequest_to_uri_links
    }
    form_excluded_columns = ['ts_created', 'ts_updated', 'requests']
    column_searchable_list = ['ts_created', 'uri.uri', 'user_agent', 'domain', 'uri.uri']
    column_list = ['ip.ip', 'uri.uri', 'user_agent', 'domain', 'ts_created']
    column_default_sort = ('ts_created', True)


class KnownIpModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    page_size = 25
    column_searchable_list = ['ip', 'name', 'last_seen', 'ts_created']
    form_excluded_columns = ['ts_created', 'ts_updated']
    column_exclude_list = ['ts_updated']
    column_default_sort = ('ts_created', True)


class OptionModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_delete = False
    can_create = False
    page_size = 25
    column_exclude_list = ['ts_created']
    form_excluded_columns = ['ts_created', 'ts_updated']
    column_list = ['name', 'value', 'ts_updated']
    column_default_sort = ('ts_updated', True)

# End File: simple-honey/app/controllers/admin.py
