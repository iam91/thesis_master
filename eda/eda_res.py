import re
import urlparse
from urllib import unquote
from functools import partial

import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")

pos_total = 0
neg_total = 0
pos_fields_stat = {}
neg_fields_stat = {}


def get_fields(field_str):
    if isinstance(field_str, str) and len(field_str) > 0:
        return dict(urlparse.parse_qsl(unquote(field_str)))
    else:
        return None


def field_cnt(data):
    global pos_total 
    global neg_total
    global pos_fields_stat
    global neg_fields_stat

    target = data['target']
    fields = get_fields(data['fields'])
    if target == 1:
        stat = pos_fields_stat
        pos_total += 1
    else:
        stat = neg_fields_stat
        neg_total += 1
    if fields:
        for k in fields:
            if k in stat:
                stat[k] += 1
            else:
                stat[k] = 1


def extract_field(field_str, field):
        fields = get_fields(field_str)
        if fields and field in fields:
            return fields[field]
        else:
            return '-1'


if __name__ == '__main__':

    pos_total = 0
    neg_total = 0
    pos_fields_stat = {}
    neg_fields_stat = {}

    data_res = pd.read_csv('../data_res.txt', sep='\\')
    print 'read respond data'
    print data_res.columns
    print data_res.info()
    print '-' * 20

    ##### stats #####
    FIELD_STATS = False 
    FIELD_VALUE = False 
    FIELD_VALUE_CONTENT_TYPE = False
    FIELD_VALUE_CONTENT_LENGTH = True

    # fields statistics
    if FIELD_STATS:
        site = 'youku'
        df = data_res.loc[data_res['site'] == site, ['target', 'fields']]
        df[['target', 'fields']].apply(field_cnt, axis=1)
        threshold = 0
        pos_fields_ratio = [(x[0], float(x[1]) / pos_total) for x in pos_fields_stat.items()]
        neg_fields_ratio = [(x[0], float(x[1]) / neg_total) for x in neg_fields_stat.items()]
        
        pos_fields_ratio = sorted(filter(lambda p: p[1] >= threshold, pos_fields_ratio), \
            key=lambda x: x[1], reverse=True)
        neg_fields_ratio = sorted(filter(lambda p: p[1] >= threshold, neg_fields_ratio), \
            key=lambda x: x[1], reverse=True)

        for r in pos_fields_ratio[:10]:
            print r 
        print '-' * 20
        for r in neg_fields_ratio[:10]:
            print r

    # field value
    if FIELD_VALUE:

        sites = '163open iqiyi letv qq sohu youku'.split()
        fields = 'connection content-type content-length'.split()
        for field in fields:
            data_res[field] = data_res['fields'].map(partial(extract_field, field=field))

        if FIELD_VALUE_CONTENT_LENGTH:
            df = data_res['target site content-length'.split()]
            df = df.loc[df['content-length'] >= 0, :]
            df['content-length'] = df['content-length'].map(int)
            fig = sns.boxplot(data=df, x='site', y='content-length', hue='target', palette='Set3')
            fig.set_yscale('log')
            plt.show()

        if FIELD_VALUE_CONTENT_TYPE:
            for site in sites:
                df = data_res.loc[data_res['site'] == site, 'target site content-type'.split()]
                df = df.loc[df['content-type'] != '-1', :]
                g = df.groupby(['content-type', 'target']).size()

                title = 'Statistics of Content-type of ' + site
                print '_'.join(title.split())

                ax = g.unstack().plot(
                    title=title,
                    kind='barh', 
                    grid=False,
                    stacked=True, 
                    edgecolor='#666666',
                    color=['#cccccc', '#666666'],
                    logx=True,
                    sort_columns=True,
                    fontsize=9,
                    width=0.8)
                plt.show()
                
    ################