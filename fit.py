#!/usr/bin/env python
# coding: utf-8

from core import scraper
from core.util import mylog
import core.model.keras.impl as kimpl
from core.util import data
import logging
import argparse
import sys
import pathlib
import os

log = mylog.get_logger("fit")

# Parse arguments

parser = argparse.ArgumentParser(
        description=(
          'Create a model and fit to a set of input data'
        ))

parser.add_argument(
        'training_data', type=str,
        help='The location of the training data file.',
        metavar='training data file')

parser.add_argument(
        '-l', '--length', type=int, help='Length of the input sequences.',
        metavar='sequence length', dest='seql', default=100)

log.debug("Arguments: {}", sys.argv)
args = parser.parse_args(sys.argv[1:])

with open(args.training_data) as f:
    inputdata = f.read()

X, y, char_map = data.preprocess(inputdata)

model = kimpl.TextGenerator(args.seql, len(char_map.keys()))
model.fit(X, y)
