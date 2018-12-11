"""Tools for processing data input to models."""

from . import mylog, strings
import numpy

log = mylog.get_logger('datautils')


def preprocess(data_container, seq_length=100):
    '''Process the input string into shape usable by the neural network.

Returns:
X: The multi-dimensional input training data.
y: The result data class in sparse vector form.
char_map: The map from input character to numeric code.'''

    # Number of distinct characters
    word_dict = len(data_container.word_map)
    word_count = len(data_container.words)

    # Create sub sequences of a fixed length to feed to network
    dataX = []
    dataY = []
    for i in range(0, word_count - seq_length):
        seq_in = data_container.words[i:i + seq_length]
        seq_out = data_container.words[i + seq_length]
        dataX.append([data_container.word_map[word] for word in seq_in])
        dataY.append(data_container.word_map[seq_out])

    n_patterns = len(dataX)
    log.debug("Total Patterns: %d", n_patterns)

    # reshape X to be [samples, time steps, features]
    X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
    # normalize
    X = X / float(word_count)

    return X, dataY


class CharacterSequence:
    """Create input sequences based on characters."""

    def __init__(self, inputstr):
        self.words = inputstr  # string is already char array basically
        chars = sorted(set(inputstr))
        # self.counts = WordSequence._count_words(self.words)
        # self.words_sorted = WordSequence._sort_words(self.counts)
        self.word_map = {c: i for i, c in enumerate(chars)}


class WordSequence:
    """Create input sequences based on words."""

    def __init__(self, inputstr):
        self.words = WordSequence._get_words_from_input(inputstr)
        self.counts = WordSequence._count_words(self.words)
        self.words_sorted = WordSequence._sort_words(self.counts)
        self.word_map = {c: i for i, c in
                         enumerate(self.counts.keys())}

    @staticmethod
    def _get_words_from_input(inputstr):

        cln = strings.clean(inputstr, strip_non_word=True)
        words = cln.split()
        return words

    @staticmethod
    def _count_words(words):
        wordmap = {w: 0 for w in words}
        for w in words:
            wordmap[w] += 1
        log.debug("Word map: %s", wordmap)
        return wordmap

    @staticmethod
    def _sort_words(word_map):

        words_sorted = sorted(word_map.keys(), reverse=True,
                              key=lambda w: word_map[w])
        return words_sorted

    def no_more_than(self, occurences):
        ftrd = [x for x in filter(
                lambda w: self.counts[w] <= occurences, self.words_sorted
                )]
        return ftrd
