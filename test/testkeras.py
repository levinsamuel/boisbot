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

        X, y, char_map = data.preprocess(testdata.inputstr)
        y = np_utils.to_categorical(y)
        log.info("y shape: %s", y.shape)
        self.assertEqual(len(char_map.keys()), y.shape[1],
                         ("The number of characters in the dictionary should "
                          "match the number number of y columns."))
        seq_length = 100
        model = kimpl.TextGenerator(seq_length, y.shape[1])
