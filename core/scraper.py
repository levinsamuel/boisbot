#!/usr/bin/env python
# coding: utf-8

import logging
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from core.types import Tweet

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

    browser = webdriver.Chrome()
    browser.get('https://twitter.com/' + user)
    log.debug("Browser size: %s", browser.get_window_rect())

    try:
        browser.find_element_by_xpath(
            "//div[@class='errorpage-body-content']/h1")
    # Error message not found, user is found
    except NoSuchElementException:
        time.sleep(1)


        body = browser.find_element_by_tag_name('body')

        twlist = WebDriverWait(
                    browser, 10).until(
                        EC.presence_of_element_located(
                            (By.ID, 'stream-items-id')
                        )
                    )

        visible = len(twlist.find_elements_by_tag_name('li'));
        log.debug("number of visible tweets: %d", visible)
        start = time.time()
        lastvis = []
        while time.time() < (start + seconds):
            lastvis.append(visible)
            for _ in range(5):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
            time.sleep(1)
            visible = len(twlist.find_elements_by_tag_name('li'));
            if len(lastvis) > 5:
                # If last five tweet counts are the same, conclude feed is done
                v = lastvis.pop(0)
                if v == visible:
                    log.info('No more tweets are loading. Exiting.')
                    break

        log.debug("tw length: %d", visible)

        tweets = []
        try:
            # find the outer div for tweets, only by requested author
            tweets = [Tweet(html) for html in browser.find_elements_by_xpath(
                "//div[contains(@class, 'tweet')][@data-screen-name='{}']".
                format(user))]
        except Exception as e:
            log.error("Failed to find tweets. Error message: {}".format(e))
            pass

    else:
        raise Exception("Page for user {} not found".format(user))
    finally:
        browser.quit()

    return tweets


def write_tweets(twts, handle):
    for slt in twts:
        handle.write(slt.cleantext + '\n')
