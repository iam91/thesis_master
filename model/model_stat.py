import pandas as pd 

from sklearn.preprocessing import MinMaxScaler

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from cv import CV

SEED = 2018
NSPLITS = 3
FEATURE_COL = 'url_len url_path_len url_path_str url_query_cnt url_query_str'.split()

if __name__ == '__main__':

    df = pd.read_csv('../data_stat.csv')    

    # data scaling
    scaler = MinMaxScaler(copy=False)

    df[FEATURE_COL] = scaler.fit_transform(df[FEATURE_COL].values)
    df.drop(['site'], axis=1, inplace=True)
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)

    dfy = df['target']
    dfx = df.drop(['target'], axis=1)

    print dfy.values.shape
    print dfx.values.shape
    print '-' * 20

    cv = CV(dfx, dfy, NSPLITS, SEED)

    # model
    clf = LogisticRegression(C=0.01)
    clf = RandomForestClassifier(n_estimators=10)
    clf = SVC(kernel='rbf', random_state=SEED, C=10.0)

    cv.validate(clf)