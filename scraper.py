#!/usr/bin/env python
# coding: utf-8

import urllib.request as req
import os, logging, sys, time, pathlib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from core.types.tweet import Tweet
import core.util.strings as strs
import argparse

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scraper")


parser=argparse.ArgumentParser(description='Scrape and print options.')
parser.add_argument('user', type=str, help='Name of the twitter user.',
                   metavar='user')
parser.add_argument('-f', '--file', type=str, metavar='file')
args=parser.parse_args(sys.argv[1:])

def findTweets(user, waits):
    """Use Selenium to scroll and find a list of tweets."""

    browser=webdriver.Chrome()
    browser.get('https://twitter.com/' + user)
    
    try:
        browser.find_element_by_xpath("//div[@class='errorpage-body-content']/h1")
    except NoSuchElementException:
        pass
    else:
        raise Exception(f"Page for user {user} not found")
    
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
        f"//div[contains(@class, 'tweet')][@data-screen-name='{user}']")
    return tweets


sltweets=findTweets(args.user, 2)

# log.setLevel(logging.DEBUG)

pathlib.Path("out").mkdir(exist_ok=True)
with open("out/tweets.txt", "w") as twtf:

    for slt in sltweets:
        sltext=slt.find_element_by_class_name('tweet-text')
        twtf.write(sltext.text + '\n')
