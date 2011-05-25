"""
Barely scratching the surface.
"""
from ostatus.hcard import hcard

def test_hcard():
    info = hcard('cdent@tiddlyspace.com')

    assert info['url'] == 'http://cdent.tiddlyspace.com/'
    assert info['fn'] == 'cdent'
    assert info['photo'] == '/recipes/cdent_public/tiddlers/SiteIcon'

