"""Admin Tools - Utilities

A collection of tools to hook into the FlaskAdmin module.
"""
from datetime import date

from flask_admin.model import typefmt

import app
from app.utilities import formatters
from app.utilities import common


def default_column_formatters():
    default_formatters = dict(typefmt.BASE_FORMATTERS)
    default_formatters.update({
        type(None): typefmt.null_formatter,
        date: formatters.date
    })
    return default_formatters


def refresh_cache_file(form, model, is_created):
    """
    Saves and reloads the cache file.
    @note The primary entry point to this method is from FlaskAdmin's "on_model_change", it should not be used outside
    of a FlaskAdmin hook.

    """
    common.save_serialized_file()
    app.global_content = common.load_cached()

# End File: simple-honey/app/utilities/admin_tools.py
