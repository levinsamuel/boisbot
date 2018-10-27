# Module for logging config

import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

log = logging.getLogger("main")

def get_logger(lgr):
    return logging.getLogger(lgr)

if __name__ == '__main__':
    print (type(log))