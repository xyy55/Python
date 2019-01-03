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
        'Cookie':'_uab_collina=152688811822362209678225; htVD_2132_connect_is_bind=0; htVD_2132_nofavfid=1; htVD_2132_smile=1D1; htVD_2132_saltkey=o826v8sm; htVD_2132_lastvisit=1529483267; _umdata=2FB0BDB3C12E491D1A01C24CA54EEFAD9CB2F1A9AD09B82BA94DC1A5B3AAB0FA80630057DE8A0967CD43AD3E795C914C9B3B828722CA97BD4825F8EED2850239; htVD_2132_auth=f42d95AQdZPmIBJ3RnpMQ5RqnFr6W2T%2FNRFfJsmKKwYgRO1VR2rMWVT2o1uMLz9UlzRRai4erTU2F6LpmWkaxzrGfuU; htVD_2132_pc_size_c=0; htVD_2132_ulastactivity=1530149807%7C0; Hm_lvt_46d556462595ed05e05f009cdafff31a=1529678618,1529917693,1530098412,1530149793; htVD_2132_ttask=603543%7C20180628; htVD_2132_lastcheckfeed=603543%7C1530149986; htVD_2132_visitedfid=2D10D8D66D16; htVD_2132_viewid=tid_755639; Hm_lpvt_46d556462595ed05e05f009cdafff31a=1530149978; htVD_2132_st_p=603543%7C1530150023%7C54632041d813c1c3de35de0b7db63948; htVD_2132_lastact=1530150040%09forum.php%09ajax',
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

        
    
    
    
    
    