import pickle
import pandas as pd 
import numpy as np

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from exp import Exp

SEED = 2018
NSPLITS = 3
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


def vectorize(trainx, validx, trainy, validy):
    v_train = TfidfVectorizer(max_df=MAX_DF, min_df=MIN_DF)
    vec_train = v_train.fit_transform(trainx).toarray()
    v_valid = TfidfVectorizer(vocabulary=v_train.vocabulary_)
    vec_valid = v_valid.fit_transform(validx).toarray()
    return vec_train, vec_valid, trainy, validy


if __name__ == '__main__':

    df = pd.read_csv('../data_text.csv')
    exp = Exp(df, preprocess)
    params = range(10, 305, 5)
    
    # models
    clfs = []

    exp.run(clfs, params, 'svm_text.csv', vectorize)
    