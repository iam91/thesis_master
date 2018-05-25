import seaborn as sns
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
sns.set(style='whitegrid')

from sklearn.feature_extraction.text import TfidfVectorizer


def termfreq(texts):
    freq = {}
    total = 0
    for t in texts:
        words = t.split()
        for w in words:
            total += 1
            if w in freq:
                freq[w] += 1
            else:
                freq[w] = 1
    freq = [(x[0], float(x[1]) / total) for x in freq.items()]
    return sorted(freq, 
        key=lambda x: float(x[1]), 
        reverse=True)


def docfreq(texts):
    freq = {}
    total = len(texts)
    for t in texts:
        words = set(t.split())
        for w in words:
            if w in freq:
                freq[w] += 1
            else:
                freq[w] = 1
    freq = [(x[0], float(x[1]) / total) for x in freq.items()]
    return sorted(freq, 
        key=lambda x: float(x[1]), 
        reverse=True)


def lenfreq(lens):
        len_cnt = {}
        for len in lens:
            if len in len_cnt:
                len_cnt[len] += 1
            else:
                len_cnt[len] = 1
        len_cnt = sorted(len_cnt.items(), key=lambda x: x[0])
        return len_cnt


def tfidf(texts, param):
    tv = TfidfVectorizer(**param)
    tf = tv.fit_transform(texts)

    idx = tv.vocabulary_.items()
    tf = np.asarray(tf.sum(axis=0)).reshape(-1)
    tf = [(x[0], tf[x[1]]) for x in idx]
    tf = sorted(tf, key=lambda x: x[1], reverse=True)[0:15]
    
    tf = pd.DataFrame(tf)
    tf.rename(columns={0: 'word', 1: 'word-ratio'}, inplace=True)
    tf['word-ratio'] = tf['word-ratio'] / tf['word-ratio'].sum()

    sns.barplot(data=tf, x='word', y='word-ratio', color='#666666')
    plt.show()


if __name__ == '__main__':

    TERM_FREQ = False 
    DOC_FREQ = True
    TF_IDF = False 

    df = pd.read_csv('../data_text.csv')
    print 'read'

    df_pos = df.loc[df['target'] == 1, :]
    df_neg = df.loc[df['target'] == 0, :]

    text_all = df['text'].values
    text_pos = df_pos['text'].values
    text_neg = df_neg['text'].values
    print df['text'].head()

    if TERM_FREQ:
        freq_pos = termfreq(text_pos)
        freq_neg = termfreq(text_neg)

        print freq_pos[0:10]
        print '-' * 20
        print freq_neg[0:10]
        print '-' * 20
        
        # lens = [len(x[0]) for x in freq_pos]
        # lens.extend([len(x[0]) for x in freq_neg])
        # len_cnt = lenfreq(lens)

    if DOC_FREQ:
        df_pos = docfreq(text_pos)
        df_neg = docfreq(text_neg)
        df_all = docfreq(text_all)

        print len(df_pos)
        print len(df_neg)
        print '-' * 20

        print df_pos[-21:-1]
        print '-' * 20
        print df_neg[-21:-1]
        print '-' * 20

        d = pd.DataFrame({'df': [x[1] for x in df_all]})
        d['seq'] = d.index
        d = d.loc[1:, :]
        print d.head()
        sns.tsplot(data=d['df'].values)
        plt.show()

    if TF_IDF:
        # tf
        param = {
            'max_df': 0.8,
            'use_idf': False,
            'norm': None
        }
        
        tf_pos = tfidf(text_pos, param)
        tf_neg = tfidf(text_neg, param)