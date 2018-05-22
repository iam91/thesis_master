import re
import urlparse
from urllib import unquote
import pandas as pd 


def split_param(url):
    parsed = urlparse.urlparse(url)
    params = [x[0] for x in urlparse.parse_qsl(parsed.query)]
    return params


def split_path(url):
    parsed = urlparse.urlparse(url)
    paths = parsed.path.split('/')[1:]
    return paths


def split_host(host):
    return host.split('.')


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
    words = []
    method = data['method']
    param = split_param(data['url'])
    path = split_path(data['url'])
    host = split_host(extract_field(data['fields'], 'host'))

    words.append(method)
    words.extend(param)
    words.extend(path)
    words.extend(host)

    return ' '.join(words).strip()



if __name__ == '__main__':
    df = pd.read_csv('data_req.txt', sep='\\')
    print 'read'
    
    df['text'] = df.apply(split, axis=1)
    df = df[['target', 'text']]
    
    print df.head()
    df.to_csv('data_text.csv', index=False, header=True)