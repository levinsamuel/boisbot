"""Tools for processing data input to models."""

import unittest
import pathlib
import shutil
from core.model.keras.impl import TextGenerator
from core.util import mylog, data
from core import types
from test import testdata
from keras.utils import np_utils

log = mylog.get_logger('testkeras')
log.setLevel(mylog.logging.INFO)
# types.log.setLevel(mylog.logging.DEBUG)


class TestKeras(unittest.TestCase):

    def test_create_model(self):

        X, y, char_map = data.preprocess(testdata.inputstr)
        y = np_utils.to_categorical(y)
        log.info("y shape: %s", y.shape)
        self.assertEqual(len(char_map.keys()), y.shape[1],
                         ("The number of characters in the dictionary should "
                          "match the number number of y columns."))
        seq_length = 100
        model = TextGenerator(seq_length, y.shape[1])

    def test_find_weights(self):

        cpath = "out/tests/checkpoints/inprocess/"
        shutil.rmtree(cpath, ignore_errors=True)
        pathlib.Path(cpath).mkdir(exist_ok=True, parents=True)
        for i in range(20):
            fn = TextGenerator.get_checkpoint_path(cpath)
            fn = fn.replace("{epoch:02d}", str(i)) \
                   .replace("{loss:.4f}", str((20-i)/10))
            lastwf = fn
            with open(fn, "x") as f:
                f.write(f"This file is a fake. Number: {i}")
        weights_file = TextGenerator.find_best_weight(cpath)
        log.info("Weights file: %s", weights_file)

        self.assertEqual(lastwf, weights_file)
