import pandas as pd 
import numpy as np

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from cv import CV

SEED = 2018
NSPLITS = 3
MAXDF = 0.5

def preprocess(df):
    df = df.copy()
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df['text']
    del df 
    return dfx, dfy


def vectorize(trainx, validx, trainy, validy):
    # low memory usage
    hv_train = HashingVectorizer(n_features=5000)
    vec_train = hv_train.fit_transform(trainx).toarray()
    hv_valid = HashingVectorizer(n_features=5000)
    vec_valid = hv_valid.fit_transform(validx).toarray()
    return vec_train, vec_valid, trainy, validy


if __name__ == '__main__':

    df = pd.read_csv('../data_text.csv')
    dfx, dfy = preprocess(df)
    
    cv = CV(dfx, dfy, NSPLITS, SEED)
    clf = RandomForestClassifier()
    valid_scores, train_scores = cv.validate(clf, vectorize)
    print train_scores
    print '-' * 20
    print valid_scores