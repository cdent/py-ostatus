
from ostatus.webfinger import finger
from ostatus.status import status

def test_webfinger():
    links = finger('cdent@tiddlyspace.com')

    assert 'http://tiddlyspace.com/profiles/cdent' in [
            link['href'] for link in links]

def test_status():
    entry = status('cdent@tiddlyspace.com')
    print entry['updated'], entry['content']
