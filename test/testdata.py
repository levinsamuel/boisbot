"""Tools for processing data input to models."""

import unittest
import logging
from functools import reduce
from core.util import mylog, data
from core.util.data import CharacterSequence, WordSequence

log = mylog.get_logger('testdatautils')

inputstr = ("yall wanna come over, play with my dog, edit a "
            "documentary im making with byyourlogic\n"
            "i would like to personally challenge conor mcgregor to a fight. "
            "i will destroy you in combat. ive been watching a lot of mma "
            "videos lately and i weigh more than you")


class TestCharacterDataUtils(unittest.TestCase):

    def setUp(self):
        log.setLevel(mylog.logging.INFO)

    def test_preprocess(self):
        # Count characters and create map to integers

        log.debug("input string: %s", inputstr)
        self.assertEqual(250, len(inputstr))
        dataseq = CharacterSequence(inputstr)

        seq_length = 100
        X, y = data.preprocess(dataseq, seq_length)
        log.debug("Output data:\nX:%s\ny:%s", X[0], y)
        log.info("Characters, seq length: %d, %d", len(inputstr), seq_length)
        log.info("X dimensions: %dx%d",
                 len(X), len(X[0]))
        self.assertEqual(250 - seq_length, len(X))

        log.debug("Output data:\nX:%s\ny:%s", X[0], y)
        log.info("Dimensions of X: %s", X.shape)


class TestWordDataUtils(unittest.TestCase):

    def setUp(self):
        log.setLevel(mylog.logging.INFO)

    def test_list_to_map(self):

        words = ['the', 'it', 'why', 'the', 'pool', 'steve', 'the', 'why']
        wordmap = WordSequence._count_words(words)
        log.info("Word map: %s", wordmap)
        self.assertEqual(3, wordmap['the'])
        self.assertEqual(1, wordmap['steve'])
        try:
            threw = False
            wordmap['nowayjose']
            self.fail("Should throw, and not get here")
        except KeyError:
            pass

    def test_count_words(self):

        log.setLevel(logging.DEBUG)
        with open("data/15min.tw", "r") as f:
            input = f.read()

        word_seq = WordSequence(input)
        log.debug("found %d distinct words.", len(word_seq.counts))
        top20 = {word_seq.words_sorted[i]:
                 word_seq.counts[word_seq.words_sorted[i]]
                 for i in range(20)}

        log.debug("20 most common: %s", top20)
        occurring_once = word_seq.no_more_than(1)
        log.debug("Number only occurring once: %d", len(occurring_once))
        twice = word_seq.no_more_than(2)
        log.debug("Number no more than twice: %d", len(twice))
