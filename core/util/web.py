from core.types import Tweet
from bs4 import BeautifulSoup as bsoup
from urllib import request as req
from core.util import mylog
import logging

log = mylog.get_logger('webutils')


def get_icon(user):

    url = page_url(user)
    tpage = req.urlopen(url=url)
    tsoup = bsoup(tpage, 'html.parser')


def query_url(user, date_before=None):

    url = (f"https://twitter.com/search?f=tweets&q=from%3A{user}"
           "%20-filter%3Aretweets%20-filter%3Areplies")
    if date_before is not None:
        url += f"%20until%3A{date_before.isoformat()}"

    return url


def page_url(user):

    return "https://twitter.com/" + user
