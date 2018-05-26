import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='ticks')
np.random.seed(sum(map(ord, "aesthetics")))

if __name__ == '__main__':

    df = pd.read_csv('rnn_text.csv')
    print 'read'
    g = sns.factorplot(data=df, x='param', y='value', hue='evaluation', legend_out=True)
    print df['param'].max()
    ticks = range(10, 300, 5)
    tick_labels = [str(x) if x % 10 == 0 else '' for x in ticks]
    g.set(xticks=range(0, len(ticks)), xticklabels=tick_labels)
    # g.set_xticklabels(rotation=45)
    plt.show()