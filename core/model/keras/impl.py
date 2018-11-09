import numpy
import pathlib
import time
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

from core.util import data, mylog
from core.types import WeightsFile

log = mylog.get_logger("kerasimpl")
log.setLevel(mylog.logging.INFO)

checkpoint_path = "out/checkpoints/inprocess/"


class TextGenerator():

    """Class to create models that can generate text from training input."""

    def __init__(self, seq_length, dictionary_size, weights_file=None,
                 user=None, layers=1):
        """Create a new LSTM model. If weights_file provided, then it will
create a pre-trained model with those weights. Otherwise it will be
untrained.

Arguments:
    user: The user this model is created for."""
        # define the LSTM model
        self.model = Sequential()
        model = self.model
        # Hardcode number of features to 1 for now
        assert layers > 0
        insh = (seq_length, 1)
        for i in range(layers):
            if i == 0:
                model.add(LSTM(256, input_shape=insh, return_sequences=True))
            else:
                model.add(LSTM(256))
            model.add(Dropout(0.2))
            # only add shape to first layer
        model.add(Dense(dictionary_size, activation='softmax'))
        if weights_file is not None:
            self.load_weights(weights_file)

        model.compile(loss='categorical_crossentropy', optimizer='adam')

        if weights_file is None:
            # If no weights, model needs to be trained, configure
            # for training, create checkpoints.
            pathlib.Path(checkpoint_path).mkdir(exist_ok=True, parents=True)
            filepath = "{}weights-{}-{}{}.hdf5".format(
                checkpoint_path, "{epoch:02d}", "{loss:.4f}",
                ("%%" + user + "%%") if user is not None else ""
            )
            checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                         save_best_only=True, mode='min')
            self.callbacks_list = [checkpoint]

    def load_weights(self, weights_file):
        """Load weights from weights file path as a string."""

        log.debug("Loading weights from file: %s", weights_file)
        model.load_weights(weights_file)

    def fit(self, X, y, epochs=20, batch_size=128):
        """Fit the model given training data X and expected result data y."""

        weights_file = find_best_weight(checkpoint_path)
        if weights_file is not None:
            self.load_weights(weights_file)
        # one hot encode the output variable
        y = np_utils.to_categorical(y)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size,
                       callbacks=self.callbacks_list)

    def predict(self, val, verbose=0):
        # @type self.model Sequential
        return self.model.predict(val, verbose=verbose)

    @staticmethod
    def find_best_weight(path):

        weights_file = None
        loss = 100
        cppath = pathlib.Path(path)
        if cppath.exists():
            fs = os.listdir(path)
            for f in fs:
                if WeightsFile.is_weights_file(f):
                    wf = WeightsFile(f)
                    if wf.loss < loss:
                        weights_file = wf.name

        return weights_file
