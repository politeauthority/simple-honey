"""test
"""

from app.models.uri import Uri
from app.models.web_request import WebRequest
from app.models.known_ip import KnownIp


def run(requested_uri):
    """
    Draws a file from the hosted files directory.

    :param path: The path of the file local to the hosted files directory.
    :type: path: str
    :returns: File contents or redirect
    """
    # thing = WebRequest.query(WebRequest.user_agent).group_by(WebRequest.user_agent).count()
    data = {
        'total_web_requests': WebRequest.query.count(),
        'total_unique_ips': KnownIp.query.count(),
        'total_unique_user_agents': WebRequest.query.distinct(WebRequest.user_agent).count(),
        # 'user_agents': thing

    }
    uris = Uri.query.filter().order_by(Uri.ts_created.desc()).limit(10).all()

    ret = []
    for u in uris:
        ret.append(u.uri)
    return str(data)
