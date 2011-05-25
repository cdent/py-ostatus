"""
Encapsulate fetching content of HTTP in one place.
"""


import httplib2
import logging

# TODO: consider caching?
HTTP = httplib2.Http()


class HTTPError(Exception):
    """
    Generic exception for presenting a problem when fetching.
    """
    pass


def fetch(uri):
    """
    Retrieve the content at uri.
    """
    response, content = HTTP.request(uri)

    if response['status'] != '200':
        logging.debug(response, content)
        raise HTTPError('bad status when fetching profile data: %s' %
                response['status'])
    else:
        return content
