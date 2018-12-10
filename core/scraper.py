#!/usr/bin/env python
# coding: utf-8

import logging
import sys
import time
import datetime as dt

from selenium.webdriver.common.keys import Keys

from core.types import Tweet
from core.util.selenium import TweetFinder

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scraper")

# Example URL using date range search:
# https://twitter.com/search?q=from%3Ajon_bois%20since%3A2000-01-01%20until%3A2018-06-01&src=typd


def find_tweets(user, seconds=120, batch_size=250, log_path=None):
    """Use Selenium to scroll and find a list of tweets.

Options:
    user: twitter user to search.
    seconds: Number of seconds to keep scrolling and collecting tweets.
    batch_size: yield tweets in batches of this size.

Returns:
    A generator of tweet array batches. Reading the tweets can be memory-
intensive, so it is recommended to read and print them in batches."""

    with TweetFinder(log_path) as finder:

        start = time.time()
        before = dt.date.fromtimestamp(start)

        if not finder.search_tweets(user):

            raise Exception("Page for user {} not found".format(user))

        while time.time() < (start + seconds):

            time.sleep(1)

            body = finder.get_body()

            visible = finder.count_visible_tweets()
            log.debug("number of visible tweets: %d", visible)
            lastvis = []
            while True:
                lastvis.append(visible)
                for _ in range(5):
                    body.send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.2)
                time.sleep(1)
                visible = finder.count_visible_tweets()

                # Exit conditions
                if len(lastvis) > 5:
                    # If last five tweet counts are the same, conclude feed is
                    # done
                    v = lastvis.pop(0)
                    if v == visible:
                        log.debug('No more tweets are loading. Exiting.')
                        break

                if visible > batch_size:

                    log.debug("Batch size reached, printing batch")
                    break

                if time.time() > (start + seconds):

                    log.debug("Time limit exceeded, exiting.")
                    break

            log.debug("tweets read this batch: %d", visible)

            try:
                # find the outer div for tweets, only by requested author
                tweets = finder.find_tweets_in_view(user)
                if len(tweets) == 0:
                    break
                # get the last in the list, earliest tweet
                before = tweets[-1].date
                log.debug("earliest tweet date: %s", before)

                if not finder.search_tweets(user, date_before=before):
                    log.debug('No tweets found before %s, exiting', before)
                    break

                yield tweets

            except Exception as e:
                log.error("Failed to find tweets. Error message: {}".format(e))
                raise

    yield tweets
