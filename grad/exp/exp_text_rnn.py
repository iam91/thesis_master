import pickle
import pandas as pd 
import numpy as np
from functools import partial

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GRU
from keras.layers import LSTM
from keras.layers import GlobalMaxPooling1D
from keras.layers.embeddings import Embedding
from keras.callbacks import EarlyStopping
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.wrappers.scikit_learn import KerasClassifier

from exp import Exp

SEED = 2018
NSPLITS = 3
NWORDS = 300
WV_DIM = 256
MAX_DF = 0.8
MIN_DF = 0.09 / 6
MAX_SEQ_LEN = 227


def preprocess(df):
    df = df.copy()
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df['text']
    del df 
    return dfx, dfy


def load_word2vec():
    f = open('word2vec.pkl', 'rb')
    word2idx = pickle.load(f)
    weights = pickle.load(f)
    return weights, word2idx


def text2idx(texts, word2idx):
    new_texts = []
    for text in texts:
        new_texts.append([word2idx[w] if w in word2idx else 0 for w in text])
    return np.array(new_texts)


def word2vec_rnn(vocab_dim, wv_dim, weights):
    embedding = Embedding(
        input_dim=vocab_dim, 
        output_dim=wv_dim, 
        weights=[weights])
    
    model = Sequential()
    model.add(embedding)
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def word2vec_sequence(trainx, validx, trainy, validy, word2idx):
    trainx = pad_sequences(text2idx(trainx, word2idx), maxlen=MAX_SEQ_LEN)
    validx = pad_sequences(text2idx(validx, word2idx), maxlen=MAX_SEQ_LEN)
    return trainx, validx, trainy, validy


def word2vec_rnn_models(vocab_dim, wv_dim, weights):
    model = KerasClassifier( \
        build_fn=word2vec_rnn, 
        vocab_dim=vocab_dim,
        wv_dim=wv_dim,
        weights=weights,
        epochs=5, 
        verbose=True,)
    return [model] 


def sequence(trainx, validx, trainy, validy):
    token = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',lower=True,split=" ", num_words=NWORDS)
    token.fit_on_texts(trainx)
    seq_train = pad_sequences(token.texts_to_sequences(trainx), maxlen=MAX_SEQ_LEN)
    seq_valid = pad_sequences(token.texts_to_sequences(validx), maxlen=MAX_SEQ_LEN)
    return seq_train, seq_valid, trainy, validy
    

def rnn(nwords, input_length):
    model = Sequential()
    model.add(Embedding(nwords, 256, input_length=input_length))
    # model.add(LSTM(128))
    model.add(GRU(128))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def rnn_models():
    model = KerasClassifier(build_fn=rnn, 
        epochs=5, 
        verbose=True, 
        nwords=NWORDS, 
        input_length=MAX_SEQ_LEN)
    return [model] 


if __name__ == '__main__':

    df = pd.read_csv('../exp_data/data_text_meth_pshuffle.csv')
    exp = Exp(df, preprocess)
    params = [0]
    early_stopping = EarlyStopping(monitor='val_loss', patience=20)
    fit_param = {
        'callbacks': [early_stopping],
        'batch_size': 128,
        'class_weight': {
            1: 0.904,
            0: 0.096
        }
    }

    # weights, word2idx = load_word2vec()
    # clfs = word2vec_rnn_models(len(word2idx) + 1, WV_DIM, weights)
    # exp.run(clfs, params, 'rnn_text_word2vec.csv', partial(word2vec_sequence, word2idx=word2idx), True, fit_param)

    clfs = rnn_models()
    exp.run(clfs, params, 'rnn_text.csv', sequence, True, fit_param)