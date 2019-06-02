import re
import sys
import urlparse
from urllib import unquote
import pandas as pd 
import numpy as np 


reg_IPv4 = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
reg_IPv6 = r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'
reg_extract_ipv4 = r'(.*):\d+'
reg_extract_ipv6 = r'\[(.*)\]:\d+'
reg_digits = r'^\d+$'
reg_codes = r'\d{2,}'

maxlen = 0

def split_param(url):
    parsed = urlparse.urlparse(url)
    params = [x[0] for x in urlparse.parse_qsl(parsed.query)]
    return params


def split_path(url):
    parsed = urlparse.urlparse(url)
    paths = parsed.path.split('/')[1:]
    if(paths[-1].find('.') > -1):
        tail = paths[-1].split('.')
        paths[-1] = tail[0]
        paths.append(tail[1])
    return paths


def extract_field(field_str, field):
        if isinstance(field_str, str) and len(field_str) > 0:
            fields = dict(urlparse.parse_qsl(unquote(field_str)))
            if field in fields:
                return fields[field]
            else:
                return ''
        else:
            return ''


def split(data):
    global maxlen
    coarse_words = []
    if 'meth' in PARTS:
        coarse_words.append(data['method'])
    if 'path' in PARTS:
        coarse_words.extend(split_path(data['url']))
    if 'para' in PARTS:
        coarse_words.extend(split_param(data['url']))
    if 'pshuffle' in PARTS:
        params = split_param(data['url'])
        np.random.shuffle(params)
        coarse_words.extend(params)

    words = []
    for w in coarse_words:
        if w in ['-', '_', '.', ',']:
            continue
        if '-' in w or '_' in w or '.' in w or ',' in w:
            words.extend(re.split(r'[\-,_\s\.]\s*', w))
        else:
            words.append(w)

    words = ['' if re.match(reg_digits, w) else w.strip('\"') for w in words]
    words = ['' if re.search(reg_codes, w) else w.strip('\"') for w in words]
    
    words = filter(lambda x: x != '' and x != '4e5f' and x != 'ae5a', words)
    words = filter(lambda x: len(x) <= 20, words)
    words = [x.lower() for x in words]

    if(len(words)) > maxlen:
        maxlen = len(words)

    return ' '.join(words).strip()


if __name__ == '__main__':

    PARTS = sys.argv[1:]
    df = pd.read_csv('../exp_data/data_req.txt', sep='\\')
    print 'read'
    
    if 'pshuffle' in PARTS:
        dfs = []
        for i in range(5):
            d = df.copy()
            d['text'] = d.apply(split, axis=1)
            dfs.append(d)
        df = pd.concat(dfs)
        df.reset_index(inplace=True)
    else: 
        df['text'] = df.apply(split, axis=1)

    df = df[['target', 'text']]
    
    print df.head()
    name = 'data_text_' + '_'.join(PARTS)
    df.to_csv('../exp_data/{:s}.csv'.format(name), index=False, header=True)
    print 'maxlen: {:d}'.format(maxlen)