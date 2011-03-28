
import httplib2

from ostatus.webfinger import finger

PROFILE = "http://webfinger.net/rel/profile-page"

HTTP = httplib2.Http()

class ProfileError(Exception):
    pass

def profile(identifier):
    links = finger(identifier)

    profile = None
    for link in links:
        if link['rel'] == PROFILE:
            profile = _get_data(link['href'])
            break

    if not profile:
        raise ProfileError('no links found to get profile')
    else:
        return profile

def _get_data(uri):
    response, content = HTTP.request(uri)

    if response['status'] != '200':
        logging.debug(response, content)
        raise StatusError('bad status when fetching profile data: %s' %
                response['status'])
    else:
        return content

