#!/usr/bin/env python
# coding: utf-8

from core import scraper
import logging
import argparse

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scrape")

# Parse arguments

parser=argparse.ArgumentParser(description='Scrape and print options.')
parser.add_argument('user', type=str, help='Name of the twitter user.',
                   metavar='user')
parser.add_argument('-f', '--file', type=str, metavar='file')
log.debug("Arguments: {}", sys.argv)
args=parser.parse_args(sys.argv[1:])

# Scrape

sltweets=scraper.find_tweets(args.user, 2)

# Print

if args.file is not None:
    pathlib.Path("out").mkdir(exist_ok=True)
    with open("out/tweets.txt", "w") as twtf:
        scraper.write_tweets(sltweets, twtf)
else:
    scraper.write_tweets(sltweets, sys.stdout)
    