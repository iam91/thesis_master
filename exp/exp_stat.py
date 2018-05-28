import pandas as pd 

from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from exp import Exp

SEED = 2018
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
    models = [SVC(kernel='rbf', random_state=SEED, C=c, class_weight={0:0.096, 1:0.904}) for c in C]
    return models


def rf_models(N):
    models = [RandomForestClassifier(n_estimators=n, random_state=SEED, class_weight={0:0.096, 1:0.904}) for n in N]
    return models


def lr_models(C):
    models = [LogisticRegression(C=c, class_weight={0:0.096, 1:0.904}) for c in C]
    return models


if __name__ == '__main__':

    df = pd.read_csv('../exp_data/data_stat.csv') 

    exp = Exp(df, preprocess)

    # model
    # params = range(10, 305, 5)
    params = [300]
    # clfs = svm_models(params)
    clfs = rf_models(params)
    # clfs = lr_models(params)
    exp.run(clfs, params, 'rf_stat_base.csv')
