import unittest
import logging
from core.util import strings, mylog

log = mylog.get_logger('stringstest')
log.setLevel(logging.DEBUG)

mytweet2 = """my favorite hitters to watch ever:

1. griffey (cleanest swing)
2. altuve (best-engineered swing)
3. vlad (batted like he was playing pong)
4. willie mcgee (swung like he wished baseball was never invented)
5. francoeur (likely had never heard of baseball)"""

mytweet3 = ("Fighting in the Age of Loneliness, a two-hour documentary i made "
            "with @ByYourLogic, is now complete. it’s one of my favorite "
            "things i’ve ever made: "
            "https://www.youtube.com/playlist?list=PLUXSZMIiUfFRSunlJERh9k1RFN"
            "nGGhnzG …pic.twitter.com/lQD6dyWdzF")


class StringsTest(unittest.TestCase):

    def test_clean(self):

        mytweet = ("we wrote a bunch of scary short stories at @sbnation. i"
                   "wrote one about a pitcher with a 0.11 era")
        result = strings.clean(mytweet)
        log.debug("Tweet 1 cleaned: %s", result)

        result = strings.clean(mytweet2)
        log.debug("Tweet 2 cleaned: %s", result)

        result = strings.clean(mytweet3, strip_urls=True)
        log.debug("Tweet 3 cleaned: %s", result)

    def test_split(self):

        words = [w for line in mytweet2.split('\n') for w in line.split(' ')]
        log.debug(words)

        words = [w for w in strings.clean(mytweet2, True).
                 replace('\n', ' \n ').split(' ')]
        log.debug(words)
