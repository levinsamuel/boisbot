#!/usr/bin/env python
# coding: utf-8

from core import scraper
from core.util import mylog, data
from core.util.data import CharacterSequence, WordSequence
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
        metavar='training_data_file')

parser.add_argument(
        '-l', '--length', type=int, help='Length of the input sequences.',
        metavar='sequence_length', dest='seql', default=100)

parser.add_argument(
        '-e', '--epochs', type=int, help='Number of training epochs.',
        metavar='epochs', dest='epochs', default=20)

parser.add_argument(
        '-b', '--batch-size', type=int,
        help='Number of samples to take each time updating gradient',
        metavar='batch_size', dest='bs', default=128)

parser.add_argument(
        '-w', '--word-based', action='store_true',
        help='analyze with words as the basic unit instead of characters',
        dest='word_based')

parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='log verbose output',
        dest='verbose')

log.debug("Arguments: {}", sys.argv)
args = parser.parse_args(sys.argv[1:])
if args.verbose:
    log.setLevel(logging.DEBUG)

with open(args.training_data) as f:
    inputdata = f.read()

data_seq = CharacterSequence(inputdata) if not args.word_based \
    else WordSequence(inputdata)

X, y = data.preprocess(data_seq)

# This import is slow, import after checking arguments.
import core.model.keras.impl as kimpl
if args.verbose:
    kimpl.log.setLevel(logging.DEBUG)

model = kimpl.TextGenerator(
    args.seql, len(data_seq.word_map.keys()), layers=2)
model.fit(X, y, epochs=args.epochs, batch_size=args.bs)
