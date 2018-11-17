import unittest
from core.util import strings, mylog
from core import scraper
from core.types import Tweet
from core.util.selenium import TweetFinder
import os

log = mylog.get_logger("testselenium")
sclog = scraper.log;
sclog.setLevel(mylog.logging.DEBUG)
#log.setLevel(mylog.logging.DEBUG)

class SeleniumTest(unittest.TestCase):

    def test_parse(self):

        user = os.environ.get("TWUSER", "deepestcat")
        sc = int(os.environ.get("SECONDS", 5))
        tweets = scraper.find_tweets(user, seconds=sc)
        log.debug("Tweets: %s", tweets)
        self.assertTrue(tweets is not None and len(tweets) > 0)

        tweet=tweets[0]
        # @type tweet Tweet
        log.debug(tweet.cleantext)
        log.debug(tweet.time)

    def test_not_found(self):

        with TweetFinder() as tf:

            # user does not exist
            self.assertFalse(tf.search_tweets("jon_boisssssss"))
            
