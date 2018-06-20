"""Admin Tools - Utilities

A collection of tools to hook into the FlaskAdmin module.
"""
from datetime import date

from flask_admin.model import typefmt

from app.utilities import formatters


def default_column_formatters():
    default_formatters = dict(typefmt.BASE_FORMATTERS)
    default_formatters.update({
        type(None): typefmt.null_formatter,
        date: formatters.date
    })
    return default_formatters

# End File: simple-honey/app/utilities/admin_tools.py
