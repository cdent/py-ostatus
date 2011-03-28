# these are not good tests, mostly there are things that drive code

from ostatus.webfinger import finger
from ostatus.status import status
from ostatus.profile import profile

def test_webfinger():
    links = finger('cdent@tiddlyspace.com')

    assert 'http://tiddlyspace.com/profiles/cdent' in [
            link['href'] for link in links]

def test_status():
    entry = status('cdent@tiddlyspace.com')
    print entry['updated'], entry['content']

def test_profile():
    data = profile('cdent@tiddlyspace.com')
    print data
