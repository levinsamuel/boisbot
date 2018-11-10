"""Types for use in project"""

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
from core.util import strings, mylog
import urllib.request as req
import os

log = mylog.get_logger("types")


class WeightsFile:

    def __init__(self, filename=None, layers=2, user=None):

        if filename is not None:
            fp = filename.rpartition('/')
            noext = fp[2].rpartition('.')[0]
            user = noext.split('%%')
            name = user[0].split('-')
            self.loss = float(name[2])
            self.epoch = int(name[1])
            if len(name) > 3:
                self.layers = int(name[3])
            self.user = None if len(user) == 1 else user[1]
            self.name = fp[2]
            self.path = fp[0]
        else:
            self.loss = "{loss:.4f}"
            self.epoch = "{epoch:02d}"
            self.user = user
            self.layers = layers
            self.path = None

        log.debug("User, loss, epoch: %s, %f, %d",
                  self.user, self.loss, self.epoch)

    def create_filename(self):
        """Get the file name for this weights file."""
        return WeightsFile._get_checkpoint_file(
            self.path, self.user, self.epoch, self.loss, self.layers
        )

    @staticmethod
    def get_checkpoint_file(cpath=None, layers=2, user=None):
        """Get the template name for the weight file."""

        wf = WeightsFile(None, layers, user)
        wf.path = cpath
        return wf.create_filename()

    def _get_checkpoint_file(cpath=None, user=None, *args):
        """Get the path to the checkpoint file"""
        filepath = "{}weights-{}{}.hdf5".format(
            (cpath + "/") if cpath is not None else "",
            '-'.join(str(a) for a in args),
            ("%%" + user + "%%") if user is not None else ""
        )
        return filepath

    @staticmethod
    def is_weights_file(f):
        return f.startswith("weights")


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
