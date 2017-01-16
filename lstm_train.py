from __future__ import absolute_import, division, print_function

import os
from six import moves
import ssl

import tflearn
from tflearn.data_utils import *

path = "short-jokes"
maxlen = 80
n
string_utf8 = open(path, "r").read().decode('utf-8')
X, Y, char_idx = \
    string_to_semi_redundant_sequences(string_utf8, seq_maxlen=maxlen, redun_step=3)

#Three layers are used here. This is possibly overkill with only
# 100,000 jokes
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

#To load the latest fitted model
#m.load("./deep_lstm_best")

seed = random_sequence_from_string(string_utf8, maxlen)

for i in range(40):                                                                                                                                               
    seed = random_sequence_from_string(string_utf8, maxlen)                                                                                                       
    m.fit(X, Y, validation_set=0.05, batch_size=512,
          n_epoch=1, run_id='rmsp_deep_uppedlr')
    m.save("saved_model" + str(i))
    print("-- TESTING...") 
    print("-- Test with temperature of 1.2 --")                                                                                                                   
    print(m.generate(maxlen, temperature=1.2, seq_seed=seed).encode('utf-8')) 
    print("-- Test with temperature of 1.0 --") 
    print(m.generate(maxlen, temperature=1.0, seq_seed=seed).encode('utf-8'))
    print("-- Test with temperature of 0.5 --") 
    print(m.generate(maxlen, temperature=0.5, seq_seed=seed).encode('utf-8')) 
