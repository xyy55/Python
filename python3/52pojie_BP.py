# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 10:28:15 2018

@author: Y
"""

from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
import random
import re
from time import sleep

base_url = "https://www.52pojie.cn/"

header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Cookie':'',
        'Host':'www.52pojie.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
comments = ["666%A3%AC%D6%A7%B3%D6%D2%BB%CF%C2%A3%A1",
            "%B8%D0%D0%BB%C2%A5%D6%F7%B7%D6%CF%ED%A3%A1",
            "%BF%B4%D7%C5%B2%BB%B4%ED%A3%A1"]
param = {
        'formhash':'531b60dd',
        'handlekey':'reply',
        'noticeauthor':'',
        'noticetrimstr':'',
        'noticeauthormsg':'',
        'usesig':'1',
        'subject':'',
        }


def get_visited_links():
    links = []
    url = base_url + "forum.php?mod=guide&view=my&type=reply&page="
    n = 0
    while(True):
        n = n + 1
        req = Request(url+str(n),headers = header)
        visited_list = urlopen(req).read()
        bs = BeautifulSoup(visited_list,'html.parser')
        raw_links = bs.find_all('th',{"class":"common"})
        if len(raw_links) == 0:
            break
        for link in raw_links:
            links.append(base_url+link.a.attrs["href"])
    return links
        
def get_new_links():
    url = base_url + 'forum.php?mod=guide&view=hot'
    req = Request(url,headers = header)
    hot_list = urlopen(req).read()
    bs = BeautifulSoup(hot_list,'html.parser')
    raw_links = bs.find_all('th',{"class":"common"})
    new_links = []
    for link in raw_links:
        link = base_url+link.a.attrs["href"]
        if link not in visited_links:
            new_links.append(link)
    return new_links

def make_comments():
    pattern = re.compile(r"thread-(.+?)-")
    raw_data = 'formhash=062ed24d&handlekey=reply&noticeauthor=&noticetrimstr=&noticeauthormsg=&usesig=1&subject=&message='.encode('utf-8')
    for raw_url in new_links:
        print(raw_url)
        tid = re.findall(pattern, raw_url)[0]
        url = 'https://www.52pojie.cn/forum.php?mod=post&infloat=yes&action=reply&fid=16&extra=&tid='+tid+'&replysubmit=yes&inajax=1'
        message = comments[random.randint(0,2)]
        data = raw_data+message.encode('utf-8')
        req = Request(url,headers = header,data=data)
        print(urlopen(req).read().decode('gbk'))
        sleep(40)
    

visited_links = get_visited_links()
new_links = get_new_links()
make_comments()

        
    
    
    
    
    
