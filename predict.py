#!/usr/bin/env python
# coding: utf-8

from core import scraper
from core.util import mylog, data
import argparse
import core.model.keras.impl as kimpl
import sys
import os
import numpy
import math
import logging

log = mylog.get_logger("predict")
log.setLevel(mylog.logging.DEBUG)

# Parse arguments

parser = argparse.ArgumentParser(
        description=(
          'Generate tweets from the input user, if weights exist to do so.'
        ))

parser.add_argument(
        'user', type=str,
        help='The user to generate tweets for.',
        metavar='twitter user')

parser.add_argument(
        'file', type=str,
        help='The file containing the original tweets that user.',
        metavar='tweet file')

parser.add_argument(
        '-n', '--number-of-chars', type=int,
        help='Number of characters to predict.',
        metavar='number of characters', dest='noc', default=140)

log.debug("Arguments: %s", sys.argv)
args = parser.parse_args(sys.argv[1:])

# Find weights file
weights = None
try:
    ind, w = -1, 100
    files = os.listdir("model")
    for i, f in enumerate(files):
        user = f.split('%%')
        name = user[0].split('-')
        loss = float(name[2])
        log.debug("User, loss: %s, %f", user[1], loss)
        ind, w = (i, loss) if user[1] == args.user and w > loss else (ind, w)
    if ind > -1:
        weights = files[ind]
except FileNotFoundError:
    pass

if weights is None:
    raise Exception("Could not find weights to load for user " + args.user)

log.debug("Using weights file: %s", weights)

with open(args.file) as f:
    inputstr = f.read()


X, y, char_map = data.preprocess(inputstr)
log.debug("X shape: %s", X.shape)
model = kimpl.TextGenerator(X.shape[1], len(char_map.keys()),
                            "model/" + weights, user=args.user)

chardict = len(char_map.keys())
revchar_map = {i: c for c, i in char_map.items()}
start = numpy.random.randint(0, X.shape[0]-1)
pat = X[start]
if log.isEnabledFor(logging.DEBUG):
    log.debug("Pattern chosen is: %s",
              ''.join(revchar_map[numpy.around(c[0]*chardict)] for c in pat))
