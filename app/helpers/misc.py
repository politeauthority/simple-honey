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
    wr.uri = '/' + request.base_url.replace(request.url_root, '')
    wr.data = data
    wr.request_type = request_type
    wr.user_agent = request.user_agent.string
    wr.ip = request.remote_addr
    wr.save()


def date_format(view, value):
    """
    """
    return value.strftime('%b %d %Y %H:%M:%S')
