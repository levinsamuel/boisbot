from core.types import Tweet
from core.util import mylog
from core.util.bsoup import Parser
from core.errors import NotFound
import logging

log = mylog.get_logger('webutils')


def get_icon(user):

    url = page_url(user)
    p = Parser(url)
    img = p.soup.find(name='img', attrs={'class': 'ProfileAvatar-image'})
    if img is None:
        raise NotFound(
            url=url,
            msg="Could not find a valid account for user: " + user)

    img_url = img.attrs['src']
    return img_url


def query_url(user, date_before=None):

    url = (f"https://twitter.com/search?f=tweets&q=from%3A{user}"
           "%20-filter%3Aretweets%20-filter%3Areplies")
    if date_before is not None:
        url += f"%20until%3A{date_before.isoformat()}"

    return url


def page_url(user):

    return "https://twitter.com/" + user
