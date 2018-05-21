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
        self.scores = {
            'precision': np.zeros(n_splits),
            'accuracy': np.zeros(n_splits),
            'recall': np.zeros(n_splits),
            'f1': np.zeros(n_splits)
        }

    def validate(self, clf):

        for i, (train_idx, valid_idx) in enumerate(self.folds.split(self.datax, self.datay)):
            print 'iter {:d}'.format(i)

            trainx, validx = self.datax.values[train_idx], self.datax.values[valid_idx]
            trainy, validy = self.datay.values[train_idx], self.datay.values[valid_idx]

            clf.fit(trainx, trainy)
            predy = clf.predict(validx)

            self.scores['precision'][i] = precision_score(validy, predy)
            self.scores['accuracy'][i] = accuracy_score(validy, predy)
            self.scores['recall'][i] = recall_score(validy, predy)
            self.scores['f1'][i] = f1_score(validy, predy)
            
        print self.scores