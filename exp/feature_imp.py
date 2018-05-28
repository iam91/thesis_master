import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
sns.set(style='whitegrid')

SEED = 2018
NSPLIT = 3
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

if __name__ == '__main__':
    np.random.seed(SEED)
    df = pd.read_csv('../exp_data/data_stat.csv')
    print 'read'
    dfx, dfy = preprocess(df)
    features = dfx.columns

    trainx, validy, trainy, validy = train_test_split(dfx, dfy, test_size=1.0 / NSPLIT, )

    clf = RandomForestClassifier(n_estimators=300, 
            class_weight={0:0.096, 1:0.904}, n_jobs=-1)

    clf.fit(trainx, trainy)
    
    importances = clf.feature_importances_

    imp = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)
    imp = pd.DataFrame(imp)

    imp.rename(columns={
        0: 'feature',
        1: 'importance'
    }, inplace=True)
        
    print imp.head()

    sns.barplot(data=imp, y='feature', x='importance', orient='h',
        facecolor='grey')
    plt.show()