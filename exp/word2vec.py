import pickle
import pandas as pd 
import numpy as np 
from gensim.models import Word2Vec

WV_DIM = 64
TF_MIN = 10

if __name__ == '__main__':

    df = pd.read_csv('../data_text.csv')
    print 'read'

    sentences = [x.split() for x in df['text'].values]
    model = Word2Vec(sentences, size=WV_DIM, min_count=TF_MIN, workers=20)

    word2idx = {w: i + 1 for i, w in enumerate(model.wv.vocab)}
    weights = np.zeros((len(model.wv.vocab) + 1, model.vector_size))
    for i, w in enumerate(model.wv.vocab):
        weights[i + 1] = model.wv[w]

    fout = open('word2vec.pkl', 'wb')
    pickle.dump(word2idx, fout)
    pickle.dump(weights, fout)
    fout.close()