"""
Profile fetching and processing.
"""

from ostatus.fetcher import fetch
from ostatus.webfinger import finger

PROFILE = "http://webfinger.net/rel/profile-page"


class ProfileError(Exception):
    """
    Report an error trying to fetch or process a profile.
    """
    pass


def profile(identifier):
    """
    Given a webfinger address, find the profile page,
    and fetch that.
    """
    links = finger(identifier)

    profile_data = None
    for link in links:
        if link['rel'] == PROFILE:
            profile_data = fetch(link['href'])
            break

    if not profile_data:
        raise ProfileError('no links found to get profile')
    else:
        return profile_data
