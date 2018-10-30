"""Tools for processing data input to models."""

import unittest
from core.util import mylog, data

log = mylog.get_logger('testdatautils')
log.setLevel(mylog.logging.INFO)

inputstr = ("yall wanna come over, play with my dog, edit a "
            "documentary im making with byyourlogic\n"
            "i would like to personally challenge conor mcgregor to a fight. "
            "i will destroy you in combat. ive been watching a lot of mma "
            "videos lately and i weigh more than you"
            )


class TestDataUtils(unittest.TestCase):

    def test_create_char_slices(self):
        # Count characters and create map to integers

        log.debug("input string: %s", inputstr)
        self.assertEqual(250, len(inputstr))

        chars = sorted(set(inputstr))
        char_map = {c: i for i, c in enumerate(chars)}
        seq_length = 100
        dataX, dataY = data.create_char_slices(inputstr, char_map, seq_length)
        log.debug("Output data:\nX:%s\ny:%s", dataX[0], dataY)
        log.info("Characters, seq length: %d, %d", len(inputstr), seq_length)
        log.info("dataX dimensions: %dx%d",
                 len(dataX), len(dataX[0]))
        self.assertEqual(250 - seq_length, len(dataX))

    def test_preprocess(self):

        X, y, char_map = data.preprocess(inputstr)
        log.debug("Output data:\nX:%s\ny:%s", X[0], y)
        log.info("Dimensions of X: %s", X.shape)
