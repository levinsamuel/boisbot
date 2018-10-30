"""Tools for processing data input to models."""

import unittest
import core.model.keras.impl as kimpl
from core.util import mylog, data
from test import testdata
from keras.utils import np_utils

log = mylog.get_logger('testkeras')
log.setLevel(mylog.logging.INFO)


class TestKeras(unittest.TestCase):

    def test_create_model(self):

        X, y = data.preprocess(testdata.inputstr)
        y = np_utils.to_categorical(y)
        log.info("y shape: %s", y.shape)

        model = kimpl.TextGenerator(100, y.shape[1])
