from urlparse import urlparse
from urlparse import parse_qs

import pandas as pd 

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


if __name__ == '__main__':
    data_req = pd.read_csv('data_req.txt', sep='\\')
    print 'read'

    data_req['url_len'] = data_req['url'].str.len()
    data_req['url_path_len'] = data_req['url'].apply(url_path)
    data_req['url_path_str'] = data_req['url'].apply(url_path_str)    
    data_req['url_query_cnt'] = data_req['url'].apply(url_query)
    data_req['url_query_str'] = data_req['url'].apply(url_query_str)    

    cols = 'target site host_is_ip url_len url_path_len url_path_str url_query_cnt url_query_str'.split()
    df = data_req[cols]

    df.to_csv('data_stat.csv', header=True, index=False)