"""Tweet wrapper object for parsing html."""

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
from core.util import strings
import urllib.request as req


class Tweet:
    """Tweet wrapper object for parsing html."""

    def __init__(self, soup):

        if isinstance(soup, BeautifulSoup):
            self.soup_text = soup.find(name='p', attrs={'class': 'tweet-text'})
            self.time = int(soup.find(name='small', attrs={'class': 'time'}).
                            findChild(name='a').
                            findChild(name='span').attrs['data-time'])
        elif isinstance(soup, WebElement):
            self.soup_text = soup.find_element_by_class_name('tweet-text')
            self.time = int(soup.find_element_by_xpath(
                                "//small[@class='time']/a/span"
                            ).get_attribute("data-time"))
        else:
            raise Exception("Unsupported parser type: {}".format(type(soup)))

        self.text = self.soup_text.text
        cl = self.text
        # not sure strip url is working well
        cl = strings.strip_url(cl)
        self.cleantext = strings.clean(cl)


def get_tweets(page):
    page = req.urlopen(url=page)
    soup = BeautifulSoup(page, 'html.parser')
    outertwts = soup.findAll(name='div',
                             attrs={'class': 'tweet',
                                    'data-screen-name': 'jon_bois'}
                             )

    tweets = [Tweet(s) for s in outertwts]
    return tweets
