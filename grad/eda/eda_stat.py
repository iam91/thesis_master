from urlparse import urlparse
from urlparse import parse_qs

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

def url_path(url):
    parsed = urlparse(url)
    paths = parsed.path.split('/')

    if(paths[-1] == ''):
        url_path_len = len(paths) - 1
    else:
        url_path_len = len(paths)
    return url_path_len


def url_path_str(url):
    parsed = urlparse(url)

    url_path_str_len = len(parsed.path)
    return  url_path_str_len


def url_query(url):
    parsed = urlparse(url)
    queries = parse_qs(parsed.query)

    url_query_cnt = len(queries)
    return url_query_cnt


def url_query_str(url):
    parsed = urlparse(url)

    url_query_str_len = len(parsed.query)
    return url_query_str_len


def distplot(df, color, label):
    ax = sns.distplot(df, 
        hist=False,
        kde=True, 
        kde_kws={
            'color': color,
            'label': label
        })
    return ax


if __name__ == '__main__':

    data_req = pd.read_csv('../exp_data/data_req.txt', sep='\\')
    print 'read'

    print data_req.loc[data_req['target'] == 1, 'target'].count(), data_req['target'].count()
    print float(data_req.loc[data_req['target'] == 1, 'target'].count()) / data_req['target'].count()

    print data_req.groupby(['site']).size()

    data_req['url_len'] = data_req['url'].str.len()
    data_req['url_path_len'] = data_req['url'].apply(url_path)
    data_req['url_path_str'] = data_req['url'].apply(url_path_str)    
    data_req['url_query_cnt'] = data_req['url'].apply(url_query)
    data_req['url_query_str'] = data_req['url'].apply(url_query_str)    
    data_req['ratio'] = data_req['url_path_len'] / data_req['url_path_str']

    # t = data_req[['url_len', 'url_path_len', 'url_query_cnt', 'url_path_str', 'url_query_str', 'ratio']]

    ##### plot #####
    FEATURE_CONTINUOUS = True
    FEATURE_DISCRETE = False

    col = 'site host_is_ip url_len url_path_len url_path_str url_query_cnt url_query_str ratio target'.split()
    df = data_req[col]

    if FEATURE_CONTINUOUS:
        for c in 'url_len url_path_len url_path_str url_query_cnt url_query_str'.split():
            print c
        # for c in ['ratio']:
            
            neg = df.loc[df['target'] == 0, c]
            pos = df.loc[df['target'] == 1, c]

            x_min = min(neg.min(), pos.min())
            x_max = max(neg.max(), pos.max())

            ax1 = distplot(neg, color='#cccccc', label='negtive')
            ax2 = distplot(pos, color='#666666', label='positive')
            plt.show()

    if FEATURE_DISCRETE:
        df = df[['host_is_ip', 'target', 'site']]
        g = df.groupby(['site', 'target', 'host_is_ip']).size()

        g = g.unstack()
        g = g.fillna(0)
        g['total'] = g.sum(axis=1)
        g.reset_index(inplace=True)
        g.rename(columns={0: 'not_ip', 1: 'is_ip'}, inplace=True)
        g['not_ip'] = g['not_ip'] / g['total']
        g['is_ip'] = g['is_ip'] / g['total']
        g = g.drop(['total'], axis=1)
        
        g0 = g.loc[g['target'] == 0, ['site', 'is_ip', 'not_ip']]
        g0.set_index('site', inplace=True)
        g1 = g.loc[g['target'] == 1, ['site', 'is_ip', 'not_ip']]
        g1.set_index('site', inplace=True)

        ax = pd.concat(dict(pos=g1, neg=g0), axis=0).plot(kind='barh', stacked=True, color=['#666666', '#cccccc'])
        plt.xlabel('proportion')
        plt.ylabel('(target, site)')
        plt.legend(bbox_to_anchor=(0.8, 1))
        plt.show()

    ################