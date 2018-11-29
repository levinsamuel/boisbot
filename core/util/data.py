"""Tools for processing data input to models."""

from . import mylog, strings
import numpy

log = mylog.get_logger('datautils')


class CharacterSequence:
    """Create input sequences based on characters."""

    def _create_char_slices(inputstr, char_map, seq_length=100):
        '''Create all slices of length equal to seq_length from the entire input
    string, as well as the next character in an associated array.

    Returns:
        dataX: N slices of the input string in an array, each slice of length
    seq_length
        dataY: N instances of the next character after the corresponding slice in
    dataX.'''
        # Count characters and create map to integers

        charcount = len(inputstr)
        dataX = []
        dataY = []
        for i in range(0, charcount - seq_length):
            seq_in = inputstr[i:i + seq_length]
            seq_out = inputstr[i + seq_length]
            dataX.append([char_map[char] for char in seq_in])
            dataY.append(char_map[seq_out])
        n_patterns = len(dataX)
        log.debug("Total Patterns: %d", n_patterns)

        return dataX, dataY


    def preprocess(inputstr):
        '''Process the input string into shape usable by the neural network.

    Returns:
        X: The multi-dimensional input training data.
        y: The result data class in sparse vector form.
        char_map: The map from input character to numeric code.'''
        chars = sorted(set(inputstr))
        char_map = {c: i for i, c in enumerate(chars)}
        # Number of distinct characters
        chardict = len(chars)

        # Create sub sequences of a fixed length to feed to network
        seq_length = 100
        dataX, dataY = CharacterSequence._create_char_slices(inputstr, char_map, seq_length)
        n_patterns = len(dataX)
        log.debug("Total Patterns: ", n_patterns)

        # reshape X to be [samples, time steps, features]
        X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
        # normalize
        X = X / float(chardict)

        return X, dataY, char_map

class WordSequence:

    def _get_words_from_input(inputstr):

        cln = strings.clean(inputstr, strip_non_word=True)
        words = cln.split(' ')
        return WordSequence._count_words(words)

    def _count_words(words):
        wordmap = {w: 0 for w in words}
        for w in words:
            wordmap[w] += 1
        log.debug("Word map: %s", wordmap)
        return wordmap

    def _sort_words(word_map):

        words_sorted = sorted(word_map.keys(), reverse=True,
                              key=lambda w: word_map[w])
        return words_sorted


    """Create input sequences based on words."""

    def _create_char_slices(inputstr, char_map, seq_length=100):
        '''Create all slices of length equal to seq_length from the entire input
    string, as well as the next character in an associated array.

Returns:
    dataX: N slices of the input string in an array, each slice of length
seq_length
    dataY: N instances of the next character after the corresponding slice in
dataX.'''
        # Count characters and create map to integers

        wordcount = len(inputstr.split(' '))
        dataX = []
        dataY = []
        for i in range(0, charcount - seq_length):
            seq_in = inputstr[i:i + seq_length]
            seq_out = inputstr[i + seq_length]
            dataX.append([char_map[char] for char in seq_in])
            dataY.append(char_map[seq_out])
        n_patterns = len(dataX)
        log.debug("Total Patterns: %d", n_patterns)

        return dataX, dataY


    def preprocess(inputstr):
        '''Process the input string into shape usable by the neural network.

Returns:
    X: The multi-dimensional input training data.
    y: The result data class in sparse vector form.
    char_map: The map from input character to numeric code.'''

        word_counts = WordSequence._get_words_from_input(inputstr)

        word_map = {c: i for i, c in enumerate(wordcounts.keys())}
        # Number of distinct characters
        chardict = len(chars)

        # Create sub sequences of a fixed length to feed to network
        seq_length = 100
        dataX, dataY = _create_char_slices(inputstr, char_map, seq_length)
        n_patterns = len(dataX)
        log.debug("Total Patterns: ", n_patterns)

        # reshape X to be [samples, time steps, features]
        X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
        # normalize
        X = X / float(chardict)

        return X, dataY, char_map
