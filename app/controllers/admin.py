"""Admin - Controller

"""
from datetime import date

from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt

from app.helpers import misc


def date_format(view, value):
    f = misc.date_format(value)
    return f


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: misc.date_format
})


class WebRequestModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS
    can_export = True
    can_delete = False
    can_create = False
    page_size = 50
    column_exclude_list = ['ts_updated']
    column_searchable_list = ['ts_created', 'user_agent', 'ip', 'uri']
    column_default_sort = ('ts_created', True)


class OptionModelView(ModelView):
    can_delete = False
    can_create = False
    page_size = 50
    column_exclude_list = ['ts_created']
    column_default_sort = ('ts_updated', True)

# End File: simple-honey/app/controllers/admin.py
