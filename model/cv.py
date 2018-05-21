import numpy as np

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

class CV(object):
    def __init__(self, datax, datay, n_splits, seed):
        self.datax = datax
        self.datay = datay 
        self.folds = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
        self.n_splits = n_splits

    def validate(self, clf):

        valid_scores = {
            'precision': np.zeros(self.n_splits),
            'accuracy': np.zeros(self.n_splits),
            'recall': np.zeros(self.n_splits),
            'f1': np.zeros(self.n_splits)
        }

        train_scores = {
            'precision': np.zeros(self.n_splits),
            'accuracy': np.zeros(self.n_splits),
            'recall': np.zeros(self.n_splits),
            'f1': np.zeros(self.n_splits)
        }

        for i, (train_idx, valid_idx) in enumerate(self.folds.split(self.datax, self.datay)):
            print 'iter {:d}'.format(i)

            trainx, validx = self.datax.values[train_idx], self.datax.values[valid_idx]
            trainy, validy = self.datay.values[train_idx], self.datay.values[valid_idx]

            clf.fit(trainx, trainy)
            pred_valid = clf.predict(validx)
            pred_train = clf.predict(trainx)

            valid_scores['precision'][i] = precision_score(validy, pred_valid)
            valid_scores['accuracy'][i] = accuracy_score(validy, pred_valid)
            valid_scores['recall'][i] = recall_score(validy, pred_valid)
            valid_scores['f1'][i] = f1_score(validy, pred_valid)

            train_scores['precision'][i] = precision_score(trainy, pred_train)
            train_scores['accuracy'][i] = accuracy_score(trainy, pred_train)
            train_scores['recall'][i] = recall_score(trainy, pred_train)
            train_scores['f1'][i] = f1_score(trainy, pred_train)
            
        return valid_scores, train_scores