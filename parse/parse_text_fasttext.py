import sys 
import pandas as pd 

def format(data):
    val = '__label__{:d} {:s}'.format(data['target'], data['text'])
    return val 

if __name__ == '__main__':
    PARTS = sys.argv[1:]    
    df = pd.read_csv('../exp_data/data_text_{:s}.csv'.format('_'.join(PARTS)))

    formatted = df.apply(format, axis=1)
    df = df['text']

    print formatted.head()
    print '-' * 20
    print df.head()
    formatted.to_csv('../exp_data/data_text_{:s}.txt'.format('_'.join(PARTS)), index=False, header=False)
    df.to_csv('../exp_data/data_text_test_{:s}.txt'.format('_'.join(PARTS)), index=False, header=False)