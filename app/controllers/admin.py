"""Admin - Controller

"""
from datetime import date

from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask_admin.form import SecureForm

from app.helpers import misc


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: misc.date_format
})


class WebRequestModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_export = True
    can_create = False
    page_size = 50
    column_exclude_list = ['ts_updated']
    column_searchable_list = ['ts_created', 'user_agent', 'ip', 'uri']
    form_excluded_columns = ['ts_created', 'ts_updated']
    column_list = ['uri', 'ip', 'platform', 'browser_name', 'ts_created']
    column_default_sort = ('ts_created', True)


class OptionModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_delete = False
    can_create = False
    page_size = 50
    column_exclude_list = ['ts_created']
    form_excluded_columns = ['ts_created', 'ts_updated']
    column_list = ['name', 'value', 'ts_updated']
    column_default_sort = ('ts_updated', True)


class RedirectionModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    page_size = 50
    form_excluded_columns = ['ts_created', 'ts_updated']
    column_exclude_list = ['ts_updated']
    column_default_sort = ('ts_created', True)


class KnownIpModelView(ModelView):
    form_base_class = SecureForm
    column_type_formatters = MY_DEFAULT_FORMATTERS
    page_size = 50
    form_excluded_columns = ['ts_created', 'ts_updated']
    column_exclude_list = ['ts_updated']
    column_default_sort = ('ts_created', True)

# End File: simple-honey/app/controllers/admin.py
