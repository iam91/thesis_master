#! /usr/bin/env python

import re
from os import listdir
from os.path import isfile, join

data_dir = '../data'
data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]

PACKET_TYPE = 0
PACKET_NUMBER = 1
PACKET_TIME = 2
PACKET_SRC_IP = 3
PACKET_DST_IP = 4

PACKET_REQ_URL = 7

ip_target = set()
ip_total = set()

def istarget(url):
    return url.startswith('/play.videocache.lecloud.com') \
            \
                or url.startswith('/m3u8') \
                or url.startswith('/videos') \
            \
                or url.find('.mp4?') != -1 \
            \
                or url.startswith('/sohu/v') \
            \
                or url.startswith('/vhot2.qqvideo.tc.qq.com') \
            \
                or url.startswith('/open-movie')

if __name__ == '__main__':
    for data_file in data_files:
        fin = open(join(data_dir, data_file), 'r')

        for line in fin.readlines():
            parts = line.strip('\n').split('\\')
            pack_type = parts[PACKET_TYPE]

            if pack_type == '1':
                ip = parts[PACKET_DST_IP]
                url = parts[PACKET_REQ_URL]

                ip_total.add(ip)

                if(istarget(url)):
                    ip_target.add(ip)

    print('total: {:d}'.format(len(ip_total)))
    print('target: {:d}'.format(len(ip_target)))

    fout = open('../exp_data/target_ip.txt', 'w')
    fout.write('\n'.join(ip_target))
    fout.close()

