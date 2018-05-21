import re
import urlparse
from urllib import unquote
from os import listdir
from os.path import isfile, join

data_dir = 'data'
data_files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]

reg_site = r'(\d*[a-z]+)\d+\.txt'
reg_IPv4 = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
reg_IPv6 = r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$'

sep = '\\'

header_req = sep.join([
    'target', 
    'site', 
    'host_is_ip',
    'type', 
    'no',
    'time',
    'src',
    'dst',
    'len',
    'method',
    'url',
    'fields'])
header_res = sep.join([
    'target', 
    'site', 
    'type', 
    'no',
    'time',
    'src',
    'dst',
    'len',
    'status',
    'fields'])

PACKET_TYPE = 0
PACKET_SRC_IP = 3
PACKET_DST_IP = 4
PACKET_REQ_FIELDS = 8

ip_target = set()

def is_ip(host):
    if(re.match(reg_IPv4, host) or re.match(reg_IPv6, host)):
        return '1'
    else:
        return '0'

if __name__ == '__main__':

    out_req = []
    out_res = []

    # load target ip addresses
    ip_target_file = open('target_ip.txt', 'r')
    for ip in ip_target_file.readlines():
        ip_target.add(ip.strip('\n'))

    # load data
    for data_file in data_files:
        fin = open(join(data_dir, data_file), 'r')

        parse_site = re.search(reg_site, data_file)
        if parse_site:
            site = parse_site.group(1)
        print site

        for line in fin.readlines():
            line = line.strip('\n')
            parts = line.split(sep)

            pack_type = parts[PACKET_TYPE]

            if pack_type == '1':
                ip = parts[PACKET_DST_IP]
                field_str = parts[PACKET_REQ_FIELDS]
                if field_str != '':
                    fields = dict(urlparse.parse_qsl(unquote(field_str)))
                    if 'host' in fields:
                        host_is_ip = is_ip(fields['host'])
                    else:
                        host_is_ip = '0'
                else:
                    host_is_ip = '0'
            else:
                ip = parts[PACKET_SRC_IP]

            if ip in ip_target:
                label = '1'
            else:
                label = '0'

            if pack_type == '1':
                line = sep.join([label, site, host_is_ip, line])
                out_req.append(line)
            else:
                line = sep.join([label, site, line])
                out_res.append(line)
    
    fout_req = open('data_req.txt', 'w')
    fout_req.write(header_req + '\n' + '\n'.join(out_req))
    fout_req.close()

    fout_res = open('data_res.txt', 'w')
    fout_res.write(header_res + '\n' + '\n'.join(out_res))
    fout_res.close()