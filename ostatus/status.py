"""
Routines for finding the latest status of a webfinger address.
"""
from ostatus.webfinger import finger
from ostatus.atom import parse_feed
from ostatus.fetcher import fetch

UPDATES_FROM = "http://schemas.google.com/g/2010#updates-from"


class StatusError(Exception):
    """
    Unable to get or parse the activity feed.
    """
    pass


def status(identifier):
    """
    Get the latest update from a webfinger address.
    """
    links = finger(identifier)

    feed = None
    for link in links:
        if link['rel'] == UPDATES_FROM:
            feed = fetch(link['href'])
            break

    if not feed:
        raise StatusError('no links found to get status')
    else:
        entries = parse_feed(feed)
        if entries:
            return entries[0]
        else:
            raise StatusError('no data for %s' % identifier)
