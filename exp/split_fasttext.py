import pandas as pd 
from sklearn.model_selection import StratifiedKFold

SEED = 2018
NSPLITS = 3
if __name__ == '__main__':

    df = pd.read_csv('../exp_data/data_text.txt', header=None)
    df_test = pd.read_csv('../exp_data/data_text_test.txt', header=None)
    df.sample(frac=1, random_state=SEED).reset_index(inplace=True)
    df_test.sample(frac=1, random_state=SEED).reset_index(inplace=True)
    
    folds = StratifiedKFold(n_splits=NSPLITS, shuffle=True, random_state=SEED)
    for i, (train_idx, valid_idx) in enumerate(folds.split(df, df)):
        train = df.iloc[train_idx]
        valid = df.iloc[valid_idx]
        test = df_test.iloc[valid_idx]

        train.to_csv('{:d}_train.txt'.format(i), index=False, header=False)
        valid.to_csv('{:d}_valid.txt'.format(i), index=False, header=False)
        test.to_csv('{:d}_test.txt'.format(i), index=False, header=False)
