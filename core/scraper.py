#!/usr/bin/env python
# coding: utf-8

import logging
import sys
import time

from selenium.webdriver.common.keys import Keys

from core.types import Tweet
from core.util.selenium import TweetFinder

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scraper")

# Example URL using date range search:
# https://twitter.com/search?q=from%3Ajon_bois%20since%3A2000-01-01%20until%3A2018-06-01&src=typd

def find_tweets(user, seconds=5):

    """
    Use Selenium to scroll and find a list of tweets.

    Options:
        user: twitter user to search.
        seconds: Number of seconds to keep scrolling and collecting tweets."""


    with TweetFinder() as finder:

        finder.search_tweets(user)

        if finder.user_found():

            time.sleep(1)

            body = finder.get_body()

            visible = finder.count_visible_tweets();
            log.debug("number of visible tweets: %d", visible)
            start = time.time()
            lastvis = []
            while time.time() < (start + seconds):
                lastvis.append(visible)
                for _ in range(5):
                    body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.2)
                time.sleep(1)
                visible = finder.count_visible_tweets();
                if len(lastvis) > 5:
                    # If last five tweet counts are the same, conclude feed is done
                    v = lastvis.pop(0)
                    if v == visible:
                        log.info('No more tweets are loading. Exiting.')
                        break

            log.debug("tw length: %d", visible)

            try:
                # find the outer div for tweets, only by requested author
                tweets = finder.find_tweets_in_view(user);
            except Exception as e:
                log.error("Failed to find tweets. Error message: {}".format(e))
                pass

        else:
            raise Exception("Page for user {} not found".format(user))

    return tweets


def write_tweets(twts, handle):
    for slt in twts:
        handle.write(slt.cleantext + '\n')
