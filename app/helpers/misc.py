"""Misc - Helpers

"""

import arrow
import os

from flask import request

from app.models.web_request import WebRequest


def record_hit():
    """
    Records the request.

    :param data: Data to be dumped into the db as a pickle object
    :type data: Anything
    """
    if request.method == 'POST':
        data = request.form['POST']
        request_type = 'POST'
    else:
        data = request.args
        request_type = 'GET'
    wr = WebRequest()
    wr.uri = request.base_url
    wr.data = data
    wr.request_type = request_type
    wr.platform = request.user_agent.platform
    wr.browser_name = request.user_agent.browser
    wr.browser_version = request.user_agent.version
    wr.browser_language = request.user_agent.language
    wr.user_agent = request.user_agent.string
    wr.ip = request.remote_addr
    wr.save()


def date_format(view, value):
    """
    Need to figure out how to get local time here and convert from UTC to that.

    :param view: Admin controller view.
    :type view: FlaskAdminView obj
    :param value: The UTC date to be converted to local time.
    :type value: datetime
    :returns: Converted datetime in pretty format.
    :rtype: str
    """
    utc = arrow.get(value, 'UTC')
    local = utc.to(os.environ.get('TZ'))
    return local.humanize()
    # return local.strftime('%b %d %Y %H:%M:%S')

# End File: simple-honey/app/helpers/misc.py
