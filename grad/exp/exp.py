import pandas as pd 
from cv import CV 

NSPLITS = 3
SEED = 2018

class Exp(object):
    def __init__(self, data, preprocess):
        dfx, dfy = preprocess(data)
        self.cv = CV(dfx, dfy, NSPLITS, SEED)

    def run(self, clfs, params, save_file=None, data_preprocess=None, validate=False, fit_param={}):

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
            valid_scores, train_scores = self.cv.validate(clf, 
                data_preprocess, 
                validate, 
                fit_param)
            valid['f1'].append(valid_scores['f1'].mean())
            valid['recall'].append(valid_scores['recall'].mean())
            train['f1'].append(train_scores['f1'].mean())
            train['recall'].append(train_scores['recall'].mean())

        valid = pd.DataFrame(valid)
        train = pd.DataFrame(train)

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

        if save_file:
            df.to_csv(save_file, header=True, index=True)