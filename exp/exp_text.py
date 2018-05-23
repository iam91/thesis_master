import pandas as pd 
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from cv import CV

SEED = 2018
NSPLITS = 3
MAXDF = 0.6

def preprocess(df):
    df = df.copy()
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df['text']
    del df 
    return dfx, dfy


def vectorize(trainx, validx, trainy, validy):
    tv_train = TfidfVectorizer(max_df=MAXDF)
    tfidf_train = tv_train.fit_transform(trainx).toarray()
    tv_valid = TfidfVectorizer(vocabulary=tv_train.vocabulary_)
    tfidf_valid = tv_valid.fit_transform(validx).toarray()

    print '-' * 20
    print tfidf_train.shape
    print tfidf_valid.shape
    print '-' * 20

    return tfidf_train, tfidf_valid, trainy, validy


if __name__ == '__main__':

    df = pd.read_csv('../data_text.csv')
    dfx, dfy = preprocess(df)
    
    cv = CV(dfx, dfy, NSPLITS, SEED)
    clf = SVC()
    valid_scores, train_scores = cv.validate(clf, vectorize)
    print valid_scores