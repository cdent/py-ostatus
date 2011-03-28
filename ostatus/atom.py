
from xml.dom import minidom

def parse_feed(feed):
    doc = minidom.parseString(feed).documentElement

    outputs = []

    entries = doc.getElementsByTagName('entry')
    for entry in entries:
        output = {}
        for child in entry.childNodes:
            try:
                name = child.tagName
            except AttributeError:
                continue
            if name in ['id', 'title', 'content', 'updated']:
                output[name] = child.childNodes[0].data
        outputs.append(output)

    return outputs
