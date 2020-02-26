# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 21:11:48 2020

@author: Y
将欧路词典单词本与不背词典单词本同步

"""

import requests
from bs4 import BeautifulSoup
import json

get_url = 'https://my.eudic.net/StudyList/WordsDataSource?draw=1&start=0&length=9999'
post_url = 'https://1tyy.cn/insertNewWord.action'
header1 = {
    "cookie": "欧路词典cookie",
    
    }
header2 = {
    'Host': '1tyy.cn',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Content-type': 'application/x-www-form-urlencoded',
    "Accept": '*/*',
    "Origin": 'https://my.eudic.net',
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    'Referer':'https://my.eudic.net/studyList',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7',
    'Cookie': '不背单词cookie'
    }

req = requests.get(get_url,headers = header1)
data = json.loads(req.text)

for i in range(0,int(data["recordsFiltered"])):
    word = data['data'][i]['uuid']
    query_url = 'https://1tyy.cn/getNewWord.action?word='+word+'&infoidx=100'
    if len(requests.get(query_url,headers = header2).text) == 2:
        print(word)
        newwordlist = {
        "word":word,
        "course":"*",
        "wordidx":"*",
        "infoidx":"100",
        "selection":"*",
        "info":'',
        "opcode":"1",    
        }
        req2 = requests.post(post_url, data = {'newwordlist':json.dumps(newwordlist)},headers = header2)
    
    