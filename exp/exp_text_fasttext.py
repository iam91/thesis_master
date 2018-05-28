import sys
import pandas as pd 
import numpy as np

from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

NSPLITS = 1

def get_label(text):
    word = text.split()
    if word[0] == '__label__0':
        return 0
    elif word[0] == '__label__1':
        return 1


if __name__ == '__main__':
    PARTS = sys.argv[1:]
    valid_scores = {
        'precision': np.zeros(NSPLITS),
        'accuracy': np.zeros(NSPLITS),
        'recall': np.zeros(NSPLITS),
        'f1': np.zeros(NSPLITS)
    }
    for i in range(NSPLITS):
        pred = pd.read_csv('{:d}_pred_{:s}.txt'.format(i, '_'.join(PARTS)), header=None)
        valid = pd.read_csv('{:d}_valid_{:s}.txt'.format(i, '_'.join(PARTS)), header=None)

        predy = pred[0].map(get_label)
        validy = valid[0].map(get_label)

        valid_scores['precision'][i] = precision_score(validy, predy)
        valid_scores['accuracy'][i] = accuracy_score(validy, predy)
        valid_scores['recall'][i] = recall_score(validy, predy)
        valid_scores['f1'][i] = f1_score(validy, predy)

    valid_f1 = pd.DataFrame({'f1': [valid_scores['f1'].mean()]})
    valid_f1.rename(columns={'f1': 'value'}, inplace=True)
    valid_f1['evaluation'] = 'valid f1'
    valid_recall = pd.DataFrame({'recall': [valid_scores['recall'].mean()]})
    valid_recall.rename(columns={'recall': 'value'}, inplace=True)
    valid_recall['evaluation'] = 'valid recall'

    df = pd.concat([valid_f1, valid_recall])
    print df.head()
    save_file = 'fasttext.csv'
    if save_file:
        df.to_csv(save_file, header=True, index=True)