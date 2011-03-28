
import httplib2

from ostatus.webfinger import finger
from ostatus.atom import parse_feed

UPDATES_FROM = "http://schemas.google.com/g/2010#updates-from"


HTTP = httplib2.Http()

class StatusError(Exception):
    pass

def status(identifier):
    links = finger(identifier)

    feed = None
    for link in links:
        if link['rel'] == UPDATES_FROM:
            feed = _get_feed(link['href'])
            break

    if not feed:
        raise StatusError('no links found to get status')
    else:
        entries = parse_feed(feed)
        if entries:
            return entries[0]
        else:
            raise StatusError('no data for %s' % identifier)

def _get_feed(uri):
    response, content = HTTP.request(uri)

    if response['status'] != '200':
        logging.debug(response, content)
        raise StatusError('bad status when fetching status feed: %s' %
                response['status'])
    else:
        return content

