import httplib2

# TODO: consider caching?
HTTP = httplib2.Http()

class HTTPError(Exception):
    pass

def fetch(uri):
    response, content = HTTP.request(uri)

    if response['status'] != '200':
        logging.debug(response, content)
        raise HTTPError('bad status when fetching profile data: %s' %
                response['status'])
    else:
        return content
