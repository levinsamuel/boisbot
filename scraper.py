#!/usr/bin/env python
# coding: utf-8

import urllib.request as req
import os, logging, sys, time, pathlib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from core.types.tweet import Tweet
import core.util.strings as strs

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scraper")

# open page from direct request
mypage='https://twitter.com/jon_bois'


def findTweets(waits):
    """Use Selenium to scroll and find a list of tweets."""
    
    browser=webdriver.Chrome()
    browser.get(mypage)
    time.sleep(1)

    body=browser.find_element_by_tag_name('body')

    for i in range(waits):
        if i > 0:
            time.sleep(3)
        for _ in range(5):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
        
        
    # find the outer div for tweets, only by requested author
    tweets=browser.find_elements_by_xpath(
        "//div[contains(@class, 'tweet')][@data-screen-name='jon_bois']")
    return tweets



sltweets=findTweets(2)

# log.setLevel(logging.DEBUG)

pathlib.Path("out").mkdir(exist_ok=True)
with open("out/tweets.txt", "w") as twtf:
    
    for slt in sltweets:
        sltext=slt.find_element_by_class_name('tweet-text')
        twtf.write(sltext.text + '\n')
