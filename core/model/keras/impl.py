import numpy
import pathlib
import time
import os
import pprint
import shutil
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

from core.util import data, mylog
from core.types import WeightsFile

log = mylog.get_logger("kerasimpl")
log.setLevel(mylog.logging.INFO)

pp = pprint.PrettyPrinter(indent=2)

checkpoint_path_default = "out/checkpoints"


class TextGenerator():

    """Class to create models that can generate text from training input."""

    def __init__(self, seq_length, dictionary_size,
                 user=None, layers=1, checkpoint_path=checkpoint_path_default):
        """Create a new LSTM model. If weights_file provided, then it will
create a pre-trained model with those weights. Otherwise it will be
untrained.

Arguments:
    user: The user this model is created for.
    layers: The number of intermediate layers to create.
    checkpoint_path: where to write checkpoint files to keep progress."""

        self.checkpoint_path = checkpoint_path + "/inprocess"

        # Find if there is an in-process weight file to start from
        weights_file = TextGenerator.find_best_weight(self.checkpoint_path)
        # If weights file provided, load layers from that file.
        if weights_file is not None:
            wf = WeightsFile(weights_file)
            # The number of intermediate layers don't count the file layer.
            log.debug(("Weights file detected: %s. "
                       "Loading layers from that file: %d"),
                      weights_file, layers)
            self.model = load_model(weights_file)
        else:
            # otherwise build model
            self.model = Sequential()

            model = self.model
            assert layers > 0
            # Hardcode number of features to 1 for now
            insh = (seq_length, 1)
            for i in range(layers):
                if i == 0:
                    model.add(LSTM(256,
                              input_shape=insh,
                              return_sequences=True))
                else:
                    model.add(LSTM(256))
                model.add(Dropout(0.2))
                # only add shape to first layer
            model.add(Dense(dictionary_size, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam')

        log.debug("Using model: %s", pp.pformat(self.model.get_config()))

        # If no weights, model needs to be trained, configure
        # for training, create checkpoints.
        pathlib.Path(self.checkpoint_path).mkdir(exist_ok=True, parents=True)
        filepath = WeightsFile.get_checkpoint_file(
                self.checkpoint_path, layers=layers,
                user=user)

        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1,
                                     save_best_only=True, mode='min')
        self.callbacks_list = [checkpoint]

    def load_weights(self, weights_file):
        """Load weights from weights file path as a string."""

        log.debug("Loading weights from file: %s", weights_file)
        self.model.load_weights(weights_file)

    def fit(self, X, y, epochs=20, batch_size=128):
        """Fit the model given training data X and expected result data y."""

        # one hot encode the output variable
        y = np_utils.to_categorical(y)
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size,
                       callbacks=self.callbacks_list)

        self.cleanup()

    def predict(self, val, verbose=0):
        # @type self.model Sequential
        return self.model.predict(val, verbose=verbose)

    def cleanup(self):
        """Move best weight to done directory and cleanup in process dir"""

        finished_weights = TextGenerator.find_best_weight(self.checkpoint_path)
        if finished_weights is not None:
            done = finished_weights.replace('inprocess', 'done')
            log.debug("Moving best weight (%s) to done folder: %s",
                      finished_weights, done)

            os.renames(finished_weights, done)
            if pathlib.Path(done).exists():
                # TODO remove in process Files
                shutil.rmtree(self.checkpoint_path, ignore_errors=True)
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

        return path + "/" + weights_file if weights_file is not None else None
