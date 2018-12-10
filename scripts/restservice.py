#!python
from core.rest import service
import argparse
import sys

parser = argparse.ArgumentParser(
        description=('Start a rest client'))
#
# parser.add_argument(
#         'training_data', type=str,
#         help='The location of the training data file.',
#         metavar='training_data_file')

parser.add_argument(
        '-p', '--prefix', type=str, help='Path to prefix routes with.',
        metavar='prefix', dest='prefix', default='')

args = parser.parse_args(sys.argv[1:])

if __name__ == '__main__':
    service.run(args.prefix)
