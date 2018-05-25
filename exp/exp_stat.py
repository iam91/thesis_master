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
    models = [SVC(kernel='rbf', random_state=SEED, C=c, class_weight={0:0.096, 1:0.904}) for c in C]
    return models


def rf_models(N):
    models = [RandomForestClassifier(n_estimators=n, random_state=SEED, class_weight={0:0.096, 1:0.904}) for n in N]
    return models


def lr_models(C):
    models = [LogisticRegression(C=c) for c in C]
    return models


if __name__ == '__main__':

    df = pd.read_csv('../data_stat.csv') 
    dfx, dfy = preprocess(df)

    cv = CV(dfx, dfy, NSPLITS, SEED)

    # model
    params = range(10, 305, 5)
    # clfs = svm_models(params)
    # clfs = rf_models(params)
    clfs = lr_models(params)
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
        valid_scores, train_scores = cv.validate(clf)
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
    df.to_csv('lr_stat.csv', header=True, index=True)

