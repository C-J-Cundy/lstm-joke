#This script imports the best set of fitted parameters for the model
#and generates some jokes from them.
#In this version I've reduced the network to two layers and 40 characters
#look-back, in order to make the network easier to train.
#I also tried out using the adam optimiser instead of RMSProp
#Note: the jokes are often very explicit and can be offensive

from __future__ import absolute_import, division, print_function

import os
from six import moves
import ssl

import tflearn
from tflearn.data_utils import *

path = "short-jokes"
maxlen = 40

string_utf8 = open(path, "r").read().decode('utf-8')
X, Y, char_idx = \
    string_to_semi_redundant_sequences(string_utf8, seq_maxlen=maxlen, redun_step=3)

g = tflearn.input_data(shape=[None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 1024, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 1024)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                       learning_rate=0.0005)

m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0)

m.load("./deep_lstm_rmsp_lessdrop-144856")
seed = random_sequence_from_string(string_utf8, maxlen)
#Experimentation found that 0.5 was the best temperature,
#but try others!
print("Temperature: 0.5")
print(m.generate(20000, temperature=0.5, seq_seed=seed))
print("Temperature: 0.8")
print(m.generate(20000, temperature=0.8, seq_seed=seed))
