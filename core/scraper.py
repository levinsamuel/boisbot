#!/usr/bin/env python
# coding: utf-8

import logging
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from core.types.tweet import Tweet

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scraper")

# Example URL using date range search:
# https://twitter.com/search?q=from%3Ajon_bois%20since%3A2000-01-01%20until%3A2018-06-01&src=typd

def find_tweets(user, seconds = 5):
    """
    Use Selenium to scroll and find a list of tweets.

    Options:
        user: twitter user to search.
        seconds: Number of seconds to keep scrolling and collecting tweets."""

    browser=webdriver.Chrome()
    browser.get('https://twitter.com/' + user)
    
    try:
        browser.find_element_by_xpath("//div[@class='errorpage-body-content']/h1")
    except NoSuchElementException:
        pass
    else:
        raise Exception("Page for user {} not found".format(user))
    
    time.sleep(1)

    body=browser.find_element_by_tag_name('body')

    start=time.time()
    while time.time() < (start + seconds):
        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        time.sleep(1)

    tweets=[]
    try:
        # find the outer div for tweets, only by requested author
        tweets=[Tweet(html) for html in browser.find_elements_by_xpath(
            "//div[contains(@class, 'tweet')][@data-screen-name='{}']".format(user))]
    except Exception as e:
        pass
    finally:
        browser.quit()
        
    return tweets
    
def write_tweets(twts, handle):
    for slt in twts:
        handle.write(slt.cleantext + '\n')
    