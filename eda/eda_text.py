import seaborn as sns
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
sns.set(style='whitegrid')

from sklearn.feature_extraction.text import TfidfVectorizer


def wordfreq(texts):
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


def tfidf(texts, param):
    tv = TfidfVectorizer(**param)
    tf = tv.fit_transform(texts)

    idx = tv.vocabulary_.items()
    tf = np.asarray(tf.sum(axis=0)).reshape(-1)
    tf = [(x[0], tf[x[1]]) for x in idx]
    tf = sorted(tf, key=lambda x: x[1], reverse=True)[0:10]
    
    tf = pd.DataFrame(tf)
    tf.rename(columns={0: 'word', 1: 'term-frequency'}, inplace=True)
    sns.barplot(data=tf, x='word', y='term-frequency', color='#666666')
    plt.show()


if __name__ == '__main__':

    SIMPLE_CNT = True  
    TF_IDF = False

    df = pd.read_csv('../data_text.csv')
    print 'read'

    df_pos = df.loc[df['target'] == 1, :]
    df_neg = df.loc[df['target'] == 0, :]

    text_all = df['text'].values
    text_pos = df_pos['text'].values
    text_neg = df_neg['text'].values
    print df['text'].head()

    if SIMPLE_CNT:
        freq_pos = wordfreq(text_pos)
        freq_neg = wordfreq(text_neg)

        print freq_pos[0:10]
        print '-' * 20
        print freq_neg[0:10]
        print '-' * 20

        lens = [len(x[0]) for x in freq_pos]
        lens.extend([len(x[0]) for x in freq_neg])
        len_cnt = {}
        for len in lens:
            if len in len_cnt:
                len_cnt[len] += 1
            else:
                len_cnt[len] = 1
        len_cnt = sorted(len_cnt.items(), key=lambda x: x[0])
        # print [x[1] for x in len_cnt]
        print len_cnt

    if TF_IDF:
        # tf
        param = {
            'max_df': 0.8,
            'use_idf': False,
            'norm': None
        }
        
        tfidf(text_pos, param)