# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 15:09:14 2018

@author: Y
"""

import requests
import json

path = "" #m3u8的文件路径
file = open(path,'r')
links = []
for i in file:
    if '#' not in i:
        i = i.strip()
        links.append(i)
file.close()
length = len(str(len(links)))
n = 0
for link in links:
    n = n + 1
    if len(str(n)) < length:
        name = '0'*(length-len(str(n))) + str(n)
    else:
        name = str(n)
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':1,
               'method':'aria2.addUri',
               'params':[[link],{"out":name+".ts","split":"5","max-connection-per-server":"16","seed-ratio":"0"}]})
    c = requests.post('http://localhost:6800/jsonrpc', jsonreq)
    print(c.text)
