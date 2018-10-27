#!/usr/bin/env python
# coding: utf-8

from core import scraper
import logging
import argparse
import sys
import pathlib
import os

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("scrape")

# Parse arguments

parser=argparse.ArgumentParser(description='Scrape and print options.')
parser.add_argument('user', type=str, help='Name of the twitter user.',
                   metavar='user')
parser.add_argument('-f', '--file', type=str, metavar='file')
parser.add_argument('-s', '--seconds', type=int, metavar='seconds',
        help='Number of seconds to keep scrolling and collecting tweets',
        default=60)
        
log.debug("Arguments: {}", sys.argv)
args=parser.parse_args(sys.argv[1:])

# Scrape

sltweets=scraper.find_tweets(args.user, args.seconds)

# Print

if args.file is not None:
    pathlib.Path("out").mkdir(exist_ok=True)
    outf="out/{}".format(args.file)
    if os.path.exists(outf):
        os.remove(outf)
    with open(outf, "w") as twtf:
        scraper.write_tweets(sltweets, twtf)
else:
    scraper.write_tweets(sltweets, sys.stdout)
    