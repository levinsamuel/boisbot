import unittest
import os
import time
import datetime as dt

from core.util import strings, mylog
from core import scraper
from core.types import Tweet
from core.util.selenium import TweetFinder

log = mylog.get_logger("testselenium")
sclog = scraper.log
sclog.setLevel(mylog.logging.INFO)
log.setLevel(mylog.logging.INFO)


class SeleniumTest(unittest.TestCase):

    def test_parse(self):

        user = os.environ.get("TWUSER", "deepestcat")
        sc = int(os.environ.get("SECONDS", 5))
        tweets = [t for tl in scraper.find_tweets(user, seconds=sc)
                  for t in tl]
        log.debug("Tweets: %s", tweets)
        self.assertTrue(tweets is not None and len(tweets) > 0)

        tweet = tweets[0]
        # @type tweet Tweet
        log.debug(tweet.cleantext)
        log.debug(tweet.time)

    def test_not_found(self):

        with TweetFinder() as tf:

            # user does not exist
            self.assertFalse(tf.search_tweets("jon_boisssssss"))

    def test_end_when_none_found(self):

        tweets = [t for tl in scraper.find_tweets('deepestcat', seconds=60)
                  for t in tl]
        log.debug("Found %d", len(tweets))


class SeleniumTestLong(unittest.TestCase):

    def test_limit(self):

        # Tweet.log.setLevel(mylog.logging.DEBUG)
        user = os.environ.get("BBTEST_USER", "jon_bois")
        secs = int(os.environ.get("BBTEST_SECONDS", 15))
        if secs == 15:
            log.info(("Long test is using default settings. Change the "
                      "user to scrape with environment variable BBTEST_USER, "
                      "and the run time with BBTEST_SECONDS."))
        start = time.time()
        numtw = 0
        for tl in scraper.find_tweets(
                user, seconds=secs, batch_size=250):

            mx = max(t.time for t in tl)
            mn = min(t.time for t in tl)
            log.debug("earliest tweet date: %s", dt.date.fromtimestamp(mn))
            log.debug("latest tweet date: %s", dt.date.fromtimestamp(mx))
            numtw += len(tl)

        end = time.time()

        log.info("Ran for %d out of %d seconds.", int(end - start), secs)
        log.info("Found %d tweets.", numtw)
