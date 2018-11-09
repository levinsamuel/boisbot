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

checkpoint_path_default = "out/checkpoints"


class TextGenerator():

    """Class to create models that can generate text from training input."""

    def __init__(self, seq_length, dictionary_size, weights_file=None,
                 user=None, layers=1, checkpoint_path=checkpoint_path_default):
        """Create a new LSTM model. If weights_file provided, then it will
create a pre-trained model with those weights. Otherwise it will be
untrained.

Arguments:
    user: The user this model is created for."""

        self.checkpoint_path = checkpoint_path + "/inprocess"
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
            pathlib.Path(self.checkpoint_path). \
                    mkdir(exist_ok=True, parents=True)
            filepath = TextGenerator.get_checkpoint_file(
                    self.checkpoint_path, user)

            checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                         save_best_only=True, mode='min')
            self.callbacks_list = [checkpoint]

    def load_weights(self, weights_file):
        """Load weights from weights file path as a string."""

        log.debug("Loading weights from file: %s", weights_file)
        model.load_weights(weights_file)

    def fit(self, X, y, epochs=20, batch_size=128):
        """Fit the model given training data X and expected result data y."""

        weights_file = TextGenerator.find_best_weight(self.checkpoint_path)
        if weights_file is not None:
            self.load_weights(weights_file)
        # one hot encode the output variable
        y = np_utils.to_categorical(y)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size,
                       callbacks=self.callbacks_list)

        self.cleanup(self.checkpoint_path)

    def predict(self, val, verbose=0):
        # @type self.model Sequential
        return self.model.predict(val, verbose=verbose)

    def cleanup(self, cpath):
        """Move best weight to done directory and cleanup in process dir"""

        finished_weights = TextGenerator.find_best_weight(self.checkpoint_path)
        done = finished_weights.replace('inprocess', 'done')
        log.debug("Moving best weight (%s) to done folder: %s",
                  finished_weights, done)

        os.renames(finished_weights, done)
        if pathlib.Path(done).exists():
            # TODO remove in process Files
            pass

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
                        loss = wf.loss

        return path + "/" + weights_file

    @staticmethod
    def get_checkpoint_file(cpath, user=None):
        """Get the path to the checkpoint file"""
        filepath = "{}/weights-{}-{}{}.hdf5".format(
            cpath, "{epoch:02d}", "{loss:.4f}",
            ("%%" + user + "%%") if user is not None else ""
        )
        return filepath
