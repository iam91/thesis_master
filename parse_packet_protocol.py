#! /usr/bin/env python

import re
from urllib import urlencode
from os import listdir
from os.path import isfile, join

textDir = 'text'
formattedDir = 'data'
textFiles = [f for f in listdir(textDir) if isfile(join(textDir, f))]

sep = '\\'

regBasic = r'\s*(\S+)\s*'
regHost = r'\s+Host:(.*)\\r\\n'
regField = r'\s+(\S+):\s(.*)\\r\\n'

BASIC_NO = 0
BASIC_TIME = 1
BASIC_SRC = 2
BASIC_DST = 3
BASIC_PROTOCOL = 4
BASIC_LEN = 5
BASIC_METHOD = 6
BASIC_STATUS = 7
BASIC_URL = 7


def parse_basics(line):
    out = {}
    basics = re.findall(regBasic, line)

    if basics[BASIC_PROTOCOL] == 'HTTP' or basics[BASIC_PROTOCOL] == 'MP4':

        if basics[BASIC_PROTOCOL] == 'MP4':
            out['type'] = False 
            out['status'] = '200'
        else:
            method = basics[BASIC_METHOD]
            if method == 'GET' or method =='POST':
                out['type'] = True
                out['method'] = method 
                out['url'] = basics[BASIC_URL]
            elif method.startswith('HTTP'):
                out['type'] = False 
                out['status'] = basics[BASIC_STATUS]
        
        if len(out) > 0:
            out['no'] = basics[BASIC_NO]
            out['time'] = basics[BASIC_TIME]
            out['src'] = basics[BASIC_SRC]
            out['dst'] = basics[BASIC_DST]
            out['len'] = basics[BASIC_LEN]
    return out


def parse_fields(line):
    fields = {}
    field = re.search(regField, line)
    if field:
        fields[field.group(1).lower()] = field.group(2)
    return fields


def out_str(out):
    out_list = []
    if out['type']:
        out_list.append('1')
    else:
        out_list.append('0')
    out_list.append(out['no'])
    out_list.append(out['time'])
    out_list.append(out['src'])
    out_list.append(out['dst'])
    out_list.append(out['len'])
    if out['type']:
        out_list.append(out['method'])
        out_list.append(out['url'])
    else:
        out_list.append(out['status'])
    out_list.append(urlencode(out['fields']))
    return sep.join(out_list)


if __name__ == '__main__':

    output = []
    for textFile in textFiles:
        print 'processing ' + textFile + ' ...'

        fin = open(join(textDir, textFile), 'r')
        fout = open(join(formattedDir, textFile), 'w')
        
        lines = fin.readlines()
        
        i = 0
        n = len(lines)

        out_lines = []
        while i < n:
            line = lines[i]
            i += 1

            out = {}
            skip = False

            # start of a packet
            if line.startswith('No'):
                line = lines[i]
                i += 1
                
                out.update(parse_basics(line))

                if len(out) > 0:
                    fields = {}
                    while i < n:
                        line = lines[i]
                        i += 1
                        
                        fields.update(parse_fields(line))

                        if line.startswith('\n'):
                            if skip:
                                break
                            else:
                                skip = True
                    out['fields'] = fields
            # end of a packet

            if len(out) > 0:
                out_lines.append(out_str(out))
        
        fout.write('\n'.join(out_lines))
        fout.close()
        fin.close()
