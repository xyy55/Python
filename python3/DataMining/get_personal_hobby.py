# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 19:43:02 2018

@author: Y
"""

import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

file = open('movie_data.json','r',encoding='utf-8')  
movie_data = json.load(file)  
file.close()  
#这里填你的豆瓣上面的id
people_name = ""
url = "https://movie.douban.com/people/"+people_name+"/"
movie_data.setdefault(people_name,{})
movie_data[people_name]["people_url"] = url


for i in range(0,6):
    comment_url_suffix = ("collect?start="+str(i*15)+"&sort=time&rating=all"
                          "&filter=all&mode=grid")
    comment_url = movie_data[people_name]["people_url"]+comment_url_suffix
    comment_data = urlopen(comment_url).read().decode('utf-8')
    bs = BeautifulSoup(comment_data,'html.parser')
    infos = bs.find("div",{"class":"grid-view"}).findAll("div",{"class":"info"})
    for info in infos:
        movie_name = info.em.get_text()
        try:
            movie_rate = re.search("[0-9]",info.findAll("li")[2].span.attrs["class"][0]).group()
        except:
            continue
        try:
            movie_comment = info.find("span",{"class":"comment"}).get_text()
        except:
            movie_comment = ""
        movie_data[people_name].setdefault("movies",{})
        movie_data[people_name]["movies"].setdefault(movie_name,{})
        movie_data[people_name]["movies"][movie_name]["movie_rate"] = movie_rate
        movie_data[people_name]["movies"][movie_name]["movie_comment"] = movie_comment

file = open('movie_data.json','w',encoding='utf-8')  
json.dump(movie_data,file,ensure_ascii=False)  
file.close() 
