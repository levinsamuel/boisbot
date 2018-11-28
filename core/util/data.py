"""Tools for processing data input to models."""

from . import mylog
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
        dataX, dataY = _create_char_slices(inputstr, char_map, seq_length)
        n_patterns = len(dataX)
        log.debug("Total Patterns: ", n_patterns)

        # reshape X to be [samples, time steps, features]
        X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
        # normalize
        X = X / float(chardict)

        return X, dataY, char_map
