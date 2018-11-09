import unittest
from core.util import strings, mylog
from core import scraper
from core.types import Tweet

log = mylog.get_logger("testselenium")
#log.setLevel(mylog.logging.DEBUG)

class SeleniumTest(unittest.TestCase):

    def test_parse(self):

        tweets=scraper.find_tweets("deepestcat")
        log.debug("Tweets: %s", tweets)
        self.assertTrue(tweets is not None and len(tweets) > 0)

        tweet=tweets[0]
        # @type tweet Tweet
        log.debug(tweet.cleantext)
        log.debug(tweet.time)
