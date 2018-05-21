import pandas as pd 

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from cv import CV

SEED = 2018
N_SPLITS = 3
FEATURE_COL = 'url_len url_path_len url_path_str url_query_cnt url_query_str'.split()

if __name__ == '__main__':

    df = pd.read_csv('../data_stat.csv')    
    scaler = MinMaxScaler(copy=False)
    kfold = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)

    df[FEATURE_COL] = scaler.fit_transform(df[FEATURE_COL].values)
    df.drop(['site'], axis=1, inplace=True)

    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df.drop(['target'], axis=1)

    print dfy.values.shape
    print dfx.values.shape
    print '-' * 20

    cv = CV(dfx, dfy, N_SPLITS, SEED)

    # model
    clf = RandomForestClassifier(n_estimators=10)
    # clf = SVC(kernel='rbf', random_state=SEED, C=50.0)

    cv.validate(clf)