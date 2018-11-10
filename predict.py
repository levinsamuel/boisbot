#!/usr/bin/env python
# coding: utf-8

from core import scraper
from core.util import mylog, data
from core.types import Tweet, WeightsFile
import argparse
from core.model.keras.impl import TextGenerator
import sys
import os
import numpy
import math
import logging

log = mylog.get_logger("predict")
log.setLevel(mylog.logging.DEBUG)
mylog.get_logger("kerasimpl").setLevel(mylog.logging.DEBUG)

# Parse arguments

parser = argparse.ArgumentParser(
        description=(
          'Generate tweets from the input user, if weights exist to do so.'
        ))

parser.add_argument(
        'user', type=str,
        help='The user to generate tweets for.',
        metavar='twitter_user')

parser.add_argument(
        'file', type=str,
        help='The file containing the original tweets that user.',
        metavar='tweet_file')

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
        wf = WeightsFile(f)
        ind, w = (i, wf.loss) \
            if wf.user == args.user and w > wf.loss \
            else (ind, w)
    if ind > -1:
        weights = files[ind]
except FileNotFoundError:
    pass

if weights is None:
    raise Exception("Could not find weights to load for user " + args.user)

log.debug("Using weights file: %s", weights)

with open(args.file) as f:
    inputstr = f.read()

# X is (No. of sequences x sequence length x 1)
X, y, char_map = data.preprocess(inputstr)
log.debug("X shape: %s", X.shape)
model = TextGenerator(X.shape[1], len(char_map.keys()),
                            "model/" + weights, user=args.user)

chardict = len(char_map.keys())
seq_length = X.shape[1]
revchar_map = {i: c for c, i in char_map.items()}
start = numpy.random.randint(0, X.shape[0]-1)
pat = list(numpy.reshape(X[start], (1, seq_length))[0])
if log.isEnabledFor(logging.DEBUG):
    log.debug(f"Type of pattern: {type(pat)}")
    log.debug("Pattern chosen is: %s",
              ''.join(revchar_map[numpy.around(c*chardict)] for c in pat))

predicted = []
for i in range(args.noc):
    inp = numpy.reshape(pat, (1, seq_length, 1))
    predic = model.predict(inp)
    ind = numpy.argmax(predic)
    predicted.append(revchar_map[ind])
    pat.append(ind/chardict)
    pat = pat[1:]

# log.debug("Predicted: %d", ind)
print(''.join(predicted))
