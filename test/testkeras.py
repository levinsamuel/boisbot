"""Tools for processing data input to models."""

import unittest
import pathlib
import shutil
import logging
from core.model.keras.impl import TextGenerator
from core.util import mylog, data
from core.util.data import CharacterSequence
from core.types import WeightsFile
from test import testdata
from keras.utils import np_utils

log = mylog.get_logger('testkeras')
log.setLevel(mylog.logging.INFO)
# types.log.setLevel(mylog.logging.DEBUG)
mylog.get_logger('kerasimpl').setLevel(logging.DEBUG)

cpath_base = "build/tests/checkpoints"


class TestKeras(unittest.TestCase):

    def __init__(self, name):

        super().__init__(name)
        data_seq = CharacterSequence(testdata.inputstr)
        X, y = data.preprocess(data_seq)
        y = np_utils.to_categorical(y)
        log.info("y shape: %s", y.shape)
        self.assertEqual(len(data_seq.word_map.keys()), y.shape[1],
                         ("The number of characters in the dictionary should "
                          "match the number number of y columns."))
        seq_length = 100
        self.model = TextGenerator(seq_length, y.shape[1],
                                   checkpoint_path=cpath_base)

    def tearDown(self):
        """Make sure files get cleaned up"""
        self.model.cleanup()

    def test_find_weights(self):

        shutil.rmtree(cpath_base, ignore_errors=True)
        cpath = cpath_base + '/inprocess'
        pathlib.Path(cpath).mkdir(exist_ok=True, parents=True)
        for i in range(20):
            fn = WeightsFile.get_checkpoint_file(cpath)
            fn = fn.replace("{epoch:02d}", str(i)) \
                   .replace("{loss:.4f}", str((20-i)/10))
            lastwf = fn
            with open(fn, "x") as f:
                f.write(f"This file is a fake. Number: {i}")
        weights_file = TextGenerator.find_best_weight(cpath)
        log.info("Weights file: %s", weights_file)

        self.assertEqual(lastwf, weights_file)

        self.assertTrue(pathlib.Path(cpath).exists())
        self.model.cleanup()
        self.assertFalse(pathlib.Path(cpath).exists())
        self.assertTrue(pathlib.Path(cpath_base + '/done').exists())
