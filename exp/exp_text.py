import pandas as pd 
import numpy as np

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.wrappers.scikit_learn import KerasClassifier

from cv import CV

SEED = 2018
NSPLITS = 3
MAX_DF = 0.8
MIN_DF = 0.0004
MAX_SEQ_LEN = 227
NWORDS = 5000

def preprocess(df):
    df = df.copy()
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df['text']
    del df 
    return dfx, dfy


def vectorize(trainx, validx, trainy, validy):
    v_train = TfidfVectorizer(max_df=MAX_DF, min_df=MIN_DF)
    vec_train = v_train.fit_transform(trainx).toarray()
    v_valid = TfidfVectorizer(vocabulary=v_train.vocabulary_)
    vec_valid = v_valid.fit_transform(validx).toarray()
    return vec_train, vec_valid, trainy, validy


def sequence(trainx, validx, trainy, validy):
    token = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',lower=True,split=" ")
    token.fit_on_texts(trainx)
    seq_train = pad_sequences(token.texts_to_sequences(trainx), maxlen=MAX_SEQ_LEN)
    seq_valid = pad_sequences(token.texts_to_sequences(validx), maxlen=MAX_SEQ_LEN)
    return seq_train, seq_valid, trainy, validy
    

def rnn(nwords, input_length):
    model = Sequential()
    model.add(Embedding(nwords, 64, input_length=input_length))
    model.add(LSTM(2))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def svm_models(C):
    models = [SVC(kernel='rbf', random_state=SEED, C=c, class_weight={0:0.096, 1:0.904}) for c in C]
    return models


def rf_models(N):
    models = [RandomForestClassifier(n_estimators=n, random_state=SEED, class_weight={0:0.096, 1:0.904}) for n in N]
    return models


def lr_models(C):
    models = [LogisticRegression(C=c, class_weight={0:0.096, 1:0.904}) for c in C]
    return models


if __name__ == '__main__':

    df = pd.read_csv('../data_text.csv')
    dfx, dfy = preprocess(df)
    
    cv = CV(dfx, dfy, NSPLITS, SEED)
    nwords = 5000
    # clf = KerasClassifier(build_fn=rnn, \
    #     epochs=3, \
    #     verbose=True, \
    #     nwords=NWORDS, \
    #     input_length=MAX_SEQ_LEN)
    # valid_scores, train_scores = cv.validate(clf, sequence)
    params = range(10, 305, 5)
    clfs = svm_models(params)
    # clfs = rf_models(params)
    # clfs = lr_models(params)
    valid = {
        'param': params,
        'f1': [],
        'recall': []
    }
    train = {
        'param': params,
        'f1': [],
        'recall': []
    }
    for clf in clfs:
        valid_scores, train_scores = cv.validate(clf, vectorize)
        valid['f1'].append(valid_scores['f1'].mean())
        valid['recall'].append(valid_scores['recall'].mean())
        train['f1'].append(train_scores['f1'].mean())
        train['recall'].append(train_scores['recall'].mean())
        # valid['f1_std'].append(valid_scores['f1'].std())
        # valid['recall_std'].append(valid_scores['recall'].std())
        # train['f1_std'].append(train_scores['f1'].std())
        # train['recall_std'].append(train_scores['recall'].std())

    valid = pd.DataFrame(valid)
    train = pd.DataFrame(train)

    print valid.head()
    print '-' * 20
    print train.head()
    print '-' * 20

    valid_f1 = valid[['param', 'f1']]
    valid_f1.rename(columns={'f1': 'value'}, inplace=True)
    valid_f1['evaluation'] = 'valid f1'
    valid_recall = valid[['param', 'recall']]
    valid_recall.rename(columns={'recall': 'value'}, inplace=True)
    valid_recall['evaluation'] = 'valid recall'
    train_f1 = train[['param', 'f1']]
    train_f1.rename(columns={'f1': 'value'}, inplace=True)
    train_f1['evaluation'] = 'train f1'
    train_recall = train[['param', 'recall']]
    train_recall.rename(columns={'recall': 'value'}, inplace=True)
    train_recall['evaluation'] = 'train recall'

    df = pd.concat([valid_f1, valid_recall, train_f1, train_recall])
    print df.head()
    df.to_csv('svm_text.csv', header=True, index=True)
    print train_scores
    print '-' * 20
    print valid_scores