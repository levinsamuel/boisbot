#!/usr/bin/env python
# coding: utf-8

from core import scraper
from core.util import mylog
import logging
import argparse
import sys
import pathlib
import os
import logging

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
parser.add_argument('-v', '--verbose', action='store_true', dest='v')
parser.add_argument(
        '-l', '--chrome-log-path', dest='log_path', type=str, metavar="path",
        help="The path to the chrome driver log file, if logging is desired.")
parser.add_argument(
        '-s', '--seconds', type=int, metavar='seconds',
        help='Number of seconds to keep scrolling and collecting tweets',
        default=60)

log.debug("Arguments: {}", sys.argv)
args = parser.parse_args(sys.argv[1:])

if args.v:
    log.setLevel(logging.DEBUG)
    scraper.log.setLevel(logging.DEBUG)


def find_and_write_tweets(user, seconds, handle):

    # Scrape
    for sltweets in scraper.find_tweets(user, seconds, log_path=args.log_path):
        # Print
        for slt in sltweets:
            handle.write(slt.cleantext + '\n')


if args.file is not None:
    pathlib.Path("out").mkdir(exist_ok=True)
    outf = "out/{}".format(args.file)
    if os.path.exists(outf):
        os.remove(outf)
    with open(outf, "w") as twtf:
        find_and_write_tweets(args.user, args.seconds, twtf)
else:
    find_and_write_tweets(args.user, args.seconds, sys.stdout)
