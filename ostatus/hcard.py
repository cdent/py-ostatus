
from ostatus.fetcher import fetch

from xml.dom import minidom

HCARD_ELEMENTS = ['fn', 'n', 'adr', 'agent', 'bday', 'category', 'class',
    'email', 'geo', 'key', 'label', 'logo', 'mailer', 'nickname', 'note',
    'org', 'photo', 'avatar', 'rev', 'role', 'sort-string', 'sound', 'tel',
    'title', 'tz', 'uid', 'url']


def hcard(uri):
    """
    Find the first hcard in a URI and parse it to usefulness.
    """

    data = fetch(uri)

    body = (minidom.parseString(data).documentElement
            .getElementsByTagName('body')[0])


    vcard = _traverse_for_class(body, 'vcard', None)
    data = _traverse_for_data(vcard)

    print data
    return data

def _traverse_for_data(element, elements=HCARD_ELEMENTS):
    results = {}
    for klass in elements:
        node = _traverse_for_class(element, klass=klass)
        if node:
            if klass == 'photo':
                data = _get_photo_src(node)
            else:
                data = _get_data(node, href=True)
            results[klass] = data

    return results

def _get_photo_src(node):
    """
    Pull the image source off a photo element.
    """
    if 'src' in node.attributes.keys():
        return node.attributes['src'].value
    else:
        return None


def _get_data(node, href=False):
    """
    Pull the text out of a node.
    """
    if href and 'href' in node.attributes.keys():
        return node.attributes['href'].value
    else:
        text = ''
        for child in node.childNodes:
            if child.nodeType == minidom.Node.TEXT_NODE:
                text += child.nodeValue
            else:
                text += _get_data(child)
        return text


def _traverse_for_class(element, klass='vcard', tracker=None):
    """
    Traverse and element looking for the first element with a 
    particular class name.
    """
    for node in element.childNodes:
        if (node.attributes
                and 'class' in node.attributes.keys()
                and klass in node.attributes['class'].value):
            tracker = node
        else:
            tracker = _traverse_for_class(node, klass, tracker)
        if tracker:
            break
    return tracker


def process_vcard(node):
    """
    extract info from a vcard
    """
    return node.toxml()
