"""
Methods for retrieving and parsing webfinger information.
"""

from xml.dom import minidom

from ostatus.fetcher import fetch


class WebFingerError(Exception):
    """
    Raised when some kind of webfinger related error needs to
    be reported.
    """
    pass


def finger(identifier):
    """
    Find the host-meta for a host and then access its
    webfinger endpoint, returning the LinkS found there.
    """
    if not identifier.startswith('acct:'):
        identifier = 'acct:%s' % identifier

    host = parse_for_host(identifier)

    host_meta = get_host_meta(host)

    template = parse_host_meta(host_meta)
    if template:
        template = template.replace('{uri}', identifier)
    else:
        raise WebFingerError('no lrdd template found')

    finger_links = _finger(template)
    links = parse_links(finger_links)

    return links


def _finger(uri):
    """Actual implementation of finger, now that we know where to look"""
    content = fetch(uri, headers={'Accept': 'application/xrd+xml'})

    doc = minidom.parseString(content).documentElement
    return doc.getElementsByTagName('Link')


def parse_links(links):
    """Turn the webfinger links into a python list of dicts."""
    link_info = []
    for link in links:
        attr_data = {}
        for attribute in link.attributes.keys():
            attr = link.attributes[attribute]
            attr_data[attr.name] = attr.value
        link_info.append(attr_data)
    return link_info


def parse_host_meta(host_meta):
    """Extract the lrdd template from host meta."""
    doc = minidom.parseString(host_meta).documentElement
    template = None
    for link in doc.getElementsByTagName('Link'):
        if link.getAttribute('rel') == 'lrdd':
            template = link.getAttribute('template')
    return template


def parse_for_host(identifier):
    """
    Get the host portion of a webfinger address.
    """
    domain = identifier.split('@')[1]
    return domain


def get_host_meta(host):
    """Ping a host for its host-meta file."""
    url = 'http://%s/.well-known/host-meta' % host
    return fetch(url)
