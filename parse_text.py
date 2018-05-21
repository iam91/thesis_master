import urlparse
import pandas as pd 


def parse_param(url):
    parsed = urlparse.urlparse(url)
    params = [x[0] for x in urlparse.parse_qsl(parsed.query)]
    return params


def parse_path(url):
    parsed = urlparse.urlparse(url)
    paths = parsed.path.split('/')[1:]
    return paths


if __name__ == '__main__':
    url = '/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/6HV8FJ6P008535RB/comments/hotList?offset=0&limit=3&showLevelThreshold=70&headLimit=1&tailLimit=2&ibc=jssdk&callback=tool10007192277292035487_1500172834387&_=1500172834388'
    print parse_param(url)
    print '-' * 20
    print parse_path(url)
    # df = pd.read_csv('data_req.txt', sep='\\')

    # text_df = df.apply(parse, axis=1)

    # text_df.to_csv('data_text.txt')