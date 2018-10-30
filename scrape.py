#!/usr/bin/env python
# coding: utf-8

from core import scraper
from core.util import mylog
import logging
import argparse
import sys
import pathlib
import os

log = mylog.get_logger("scrape")

# Parse arguments

parser = argparse.ArgumentParser(
        description=(
          'Scrape and print options. NOTE: This will launch a browser window '
          'in order to open the twitter profile and scroll through the feed. '
          'DO NOT minimize or close this window, or else the scrolling will '
          'not complete, and the tweets will not be fetched.\n\n'
        ))

parser.add_argument(
        'user', type=str, help='Name of the twitter user.',
        metavar='user')
parser.add_argument('-f', '--file', type=str, metavar='file')
parser.add_argument(
        '-s', '--seconds', type=int, metavar='seconds',
        help='Number of seconds to keep scrolling and collecting tweets',
        default=60)

log.debug("Arguments: {}", sys.argv)
args = parser.parse_args(sys.argv[1:])

# Scrape

sltweets = scraper.find_tweets(args.user, args.seconds)

# Print

if args.file is not None:
    pathlib.Path("out").mkdir(exist_ok=True)
    outf = "out/{}".format(args.file)
    if os.path.exists(outf):
        os.remove(outf)
    with open(outf, "w") as twtf:
        scraper.write_tweets(sltweets, twtf)
else:
    scraper.write_tweets(sltweets, sys.stdout)
