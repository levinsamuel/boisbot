from bs4 import BeautifulSoup as bsoup
from urllib import request as req
from urllib.error import HTTPError
from core.util import mylog
from core.errors import NotFound

log = mylog.get_logger('BeautifulSoupUtils')


class Parser:
    """Wrapper for BeautifulSoup parser. Get the direct parser with 'soup'
attribute"""

    def __init__(self, url):

        try:
            tpage = req.urlopen(url=url)
        except HTTPError as e:
            raise NotFound(parent=e)

        self.soup = bsoup(tpage, 'html.parser')
