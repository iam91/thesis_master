import pandas as pd 

from sklearn.preprocessing import MinMaxScaler

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from cv import CV

SEED = 2018
NSPLITS = 3
FEATURE_COL = 'url_len url_path_len url_path_str url_query_cnt url_query_str'.split()


def preprocess(df):
    df = df.copy()
    scaler = MinMaxScaler(copy=False)
    df[FEATURE_COL] = scaler.fit_transform(df[FEATURE_COL].values)
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df.drop(['site', 'target'], axis=1)
    del df 
    return dfx, dfy


def svm_models(C):
    models = [SVC(kernel='rbf', random_state=SEED, C=c) for c in C]
    return models


def rf_models(N):
    models = [RandomForestClassifier(n_estimators=n, random_state=SEED) for n in N]
    return models


def lr_models(C):
    models = [LogisticRegression(C=c) for c in C]
    return models


if __name__ == '__main__':

    df = pd.read_csv('../data_stat.csv') 
    dfx, dfy = preprocess(df)

    print '-' * 20
    print dfy.values.shape
    print dfx.values.shape
    print '-' * 20
    print df.info()
    print '-' * 20

    cv = CV(dfx, dfy, NSPLITS, SEED)

    # model
    clfs = svm_models([5, 10, 20, 30, 40, 50, 60, 100])
    for clf in clfs:
        valid_scores, train_scores = cv.validate(clf)
        print valid_scores
        print '-' * 20

