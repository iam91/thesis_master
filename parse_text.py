import re
import urlparse
from urllib import unquote
import pandas as pd 


reg_IPv4 = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
reg_IPv6 = r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'
reg_extract_ipv4 = r'(.*):\d+'
reg_extract_ipv6 = r'\[(.*)\]:\d+'
reg_digits = r'^\d+$'
reg_codes = r'\d{2,}'


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


def split_host(host):
    if(host.startswith('[')):
        r = re.search(reg_extract_ipv6, host)
        host = r.group(1)
    elif(host.find(':') > -1):
        r = re.search(reg_extract_ipv4, host)
        host = r.group(1)
    if re.match(reg_IPv6, host):
        seg = host.split(':')
        return map(lambda x: '0' if len(x) == 0 else x, seg)
    else:
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
    coarse_words = []
    method = data['method']
    param = split_param(data['url'])
    path = split_path(data['url'])
    host = [] # split_host(extract_field(data['fields'], 'host'))

    coarse_words.append(method)
    # coarse_words.extend(host)
    coarse_words.extend(path)
    coarse_words.extend(param)

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
    
    words = filter(lambda x: x != '', words)
    words = filter(lambda x: len(x) <= 20, words)

    return ' '.join(words).strip()



if __name__ == '__main__':
    df = pd.read_csv('data_req.txt', sep='\\')
    print 'read'
    
    df['text'] = df.apply(split, axis=1)
    df = df[['target', 'text']]
    
    print df.head()
    df.to_csv('data_text.csv', index=False, header=True)