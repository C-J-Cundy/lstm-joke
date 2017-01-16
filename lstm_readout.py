#This script imports the best set of fitted parameters for the model
#and generates some jokes from them.
#Note: the jokes are often very explicit and can be offensive

from __future__ import absolute_import, division, print_function

import os
from six import moves
import ssl

import tflearn
from tflearn.data_utils import *

path = "short-jokes"
maxlen = 80

string_utf8 = open(path, "r").read().decode('utf-8')
X, Y, char_idx = \
    string_to_semi_redundant_sequences(string_utf8, seq_maxlen=maxlen, redun_step=3)

g = tflearn.input_data(shape=[None, maxlen, len(char_idx)])
g = tflearn.lstm(g, 1024, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 1024, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 1024)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='RMSProp', loss='categorical_crossentropy',
                       learning_rate=0.0005)

m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0,
                              checkpoint_path='./deep_lstm_best',
                              tensorboard_dir='/tmp/tflearn_logs',
                              tensorboard_verbose=2)

m.load("./deep_lstm_best")
seed = random_sequence_from_string(string_utf8, maxlen)
#Experimentation found that 0.5 was the best temperature,
#but try others!
print(m.generate(20000, temperature=0.5, seq_seed=seed))

