
import httplib2
import logging

from xml.dom import minidom

HTTP = httplib2.Http()

class WebFingerError(Exception):
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
    response, content = HTTP.request(uri)

    if response['status'] != '200':
        logging.debug(response, content)
        raise WebFingerError('bad status when fingering: %s' %
                response['status'])
    else:
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
    domain = identifier.split('@')[1]
    return domain


def get_host_meta(host):
    """Ping a host for its host-meta file."""
    url = 'http://%s/.well-known/host-meta' % host

    response, content = HTTP.request(url)

    if response['status'] != '200':
        logging.debug(response, content)
        raise WebFingerError('bad status when fetch host-meta: %s' %
                response['status'])
    else:
        return content


