from __future__ import division

from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, normalization, LSTM, Convolution1D
from keras.preprocessing import sequence
from DataReader import DataReader, DataParserOpt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import StratifiedKFold
import os
import sys
import numpy as np
import pandas as pd
import inspect
import itertools
import hickle as hkl
# os.chdir('/sharedfolder/Rutgers/S17/capstone/common/LeapMotion-Sign-Language-Interpretor')
# os.chdir('LeapMotion-Sign-Language-Interpretor/')
os.chdir('/mnt/64efbe69-b915-4398-ae54-48f156ce7125/Documents/Rutgers/S17/capstone/common/LeapMotion-Sign-Language-Interpretor')
print os.getcwd()
MAX_LEN = 200
ONE_HAND = 186
NUM_CHAR = 26
SPLIT = .8

from keras.layers import LSTM, Input, merge
from keras.layers import wrappers, Convolution1D, MaxPooling1D, Flatten, Dropout
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers import merge, Lambda
from keras import backend as K
from keras.models import Model
import json
from keras.utils import plot_model


class SimpleRNN():

    def __init__(self, inputdim, model=0):
        # Should build model here
        if model == 0:
            self.smallLSTM(inputdim)
        elif model == 1:
            self.bigLSTM(inputdim)

    def bigLSTM(self, inputdim):
        inputs = Input(shape=inputdim)
        # biLSTM = wrappers.Bidirectional(LSTM(128, return_sequences=True))
        x1 = LSTM(186, return_sequences=True)(inputs)
        # x2 = LSTM(128, return_sequences=True)(x1)
        shortcut = merge([x1, inputs], mode='sum')
        x2 = LSTM(128, return_sequences=True)(shortcut)

        # biLSTM = wrappers.Bidirectional(
        #     LSTM(186, return_sequences=True))(inputs)
        # shortcut = merge([inputs, biLSTM], mode='sum')

        time_distributed_merge_layer = Lambda(function=lambda x: K.mean(x, axis=1),
                                              output_shape=lambda shape: (shape[0],) + shape[2:])
        td = time_distributed_merge_layer(x2)
        # x3 = LSTM(128, return_sequences=False)(shortcut)
        d = Dense(NUM_CHAR, activation='softmax')(td)

        self.model = Model(inputs=inputs, outputs=d)
        self.model.compile(loss='categorical_crossentropy', optimizer='Adam',
                           metrics=['accuracy'])

    def smallLSTM(self, inputdim):

        self.model = Sequential()

        # Working code DO NOT CHANGE
        # self.model.add(wrappers.TimeDistributed(
        #     Dense(32, activation='relu'), input_shape=inputdim))
        # self.model.add(Convolution1D(32, 3, border_mode='valid',
        # subsample_length=1, activation='relu', input_shape=inputdim))
        self.model.add(wrappers.Bidirectional(
            LSTM(128, return_sequences=True), input_shape=inputdim))
        # self.model.add(Dropout(.2))
        # self.model.add(wrappers.Bidirectional(
        #     LSTM(128, return_sequences=False)
        # ))
        # self.model.add(LSTM(64))
        time_distributed_merge_layer = Lambda(function=lambda x: K.mean(x, axis=1),
                                              output_shape=lambda shape: (shape[0],) + shape[2:])
        self.model.add(time_distributed_merge_layer)

        # self.model.add(LSTM(32))
        self.model.add(Dense(NUM_CHAR))
        # self.model.add(Dropout(.25))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='Adam',
                           metrics=['accuracy'])

        # pass
    def train(self, X, y, X_val, y_val, num_epoch=150):
        # TODO: define input arguments,
        # should take in a generator that gives a batch
        return self.model.fit(X, y, batch_size=64, nb_epoch=num_epoch,
                              shuffle=True, validation_data=(X_val, y_val), verbose=1)

    def eval(self, X, y):
        return self.model.evaluate(X, y, verbose=1)

    def save(self, name):
        self.model.save(name + '.h5')

    def load(self, filename):
        self.model = load_model(filename)

    def draw(self, name):
        plot_model(self.model, to_file=name)

# p = np.random.permutation(len(data_))


data_ = np.load('data_normalized.npy')
y_mat = np.load('label_new.npy')
# p = np.load('p.npy')
# data_r = data_[p]
# y_mat_r = y_mat[p]
N = len(data_)
# print np.unique(np.argmax(y_mat_r[int(N * 0.75):], axis=1)).shape
# print np.bincount(np.sort(np.argmax(y_mat_r[int(N2 * 0.75):], axis=1)))
# print data_.shape, y_mat.shape, np.argmax(y_mat, axis=1).shape

skf = StratifiedKFold(n_splits=5, shuffle=True)

models = [0, 1]
for i in models:
    hist = []
    bestAcc = 0.0
    bestModel = None
    for train, test in skf.split(np.zeros(N), np.argmax(y_mat, axis=1)):
        myNet = SimpleRNN((MAX_LEN, ONE_HAND), i)
        hist.append(myNet.train(data_[train], y_mat[
                    train], data_[test], y_mat[test], 150))

        if hist[-1].history['val_acc'][-1] > bestAcc:
            bestAcc = hist[-1].history['val_acc'][-1]
            bestModel = myNet
    bestModel.save(str(i) + '_normalized')
    # bestModel.draw(str(i) + '.png')
    with open('history{}.txt'.format(i), 'w') as outfile:
        json.dump([i.history['val_acc'] for i in hist], outfile)
