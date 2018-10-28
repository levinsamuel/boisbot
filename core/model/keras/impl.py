import numpy
import pathlib
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

from core.util import data

class TextGenerator():

    def __init__(self):
        # define the LSTM model
        self.model = Sequential()
        model=self.model
        model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        pathlib.Path("out/checkpoints").mkdir(exist_ok=True)
        filepath="out/checkpoints/weights-{epoch:02d}-{loss:.4f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        self.callbacks_list = [checkpoint]

    def fit(self, X, y):
        self.model.fit(X, y, epochs=20, batch_size=128, callbacks=self.callbacks_list)

# Fit model
model=TextGenerator()
model.fit(X, y)
