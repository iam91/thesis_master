import pandas as pd 

def format(data):
    val = '__label__{:d} {:s}'.format(data['target'], data['text'])
    return val 

if __name__ == '__main__':
    
    df = pd.read_csv('data_text.csv')

    formatted = df.apply(format, axis=1)
    df = df['text']

    print formatted.head()
    print '-' * 20
    print df.head()
    formatted.to_csv('data_text.txt', index=False, header=False)
    df.to_csv('data_text_test.txt', index=False, header=False)