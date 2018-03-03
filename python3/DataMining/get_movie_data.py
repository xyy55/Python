# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 10:28:50 2018

@author: Y
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json

people_names = []
people_urls = []
r = re.compile(r'e/(.+)/')
for i in range(0,5):
    url = ("https://movie.douban.com/subject/26862829/comments?"
          "start="+str(i*20)+"&limit=20&sort=new_score&status=P&percent_type=")
    data = urlopen(url).read().decode('utf-8')
    bs = BeautifulSoup(data,'html.parser')
    comments = bs.findAll("div",{"class":"comment"})
    for comment in comments:
        people_url = comment.findAll("a")[1].attrs["href"].replace("www","movie")
        name = re.findall(r,people_url)[0]
        people_names.append(name)
        people_urls.append(people_url)

final_data = {}
for i in range(0,len(people_names)):
    final_data.setdefault(people_names[i],{})
    final_data[people_names[i]]["people_url"] = people_urls[i]


for people_name in final_data:
    print(people_name)
    for i in range(0,6):
        comment_url_suffix = ("collect?start="+str(i*15)+"&sort=time&rating=all"
                              "&filter=all&mode=grid")
        comment_url = final_data[people_name]["people_url"]+comment_url_suffix
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
            final_data[people_name].setdefault("movies",{})
            final_data[people_name]["movies"].setdefault(movie_name,{})
            final_data[people_name]["movies"][movie_name]["movie_rate"] = movie_rate
            final_data[people_name]["movies"][movie_name]["movie_comment"] = movie_comment
            
            

file = open('movie_data.json','w',encoding='utf-8')  
  
json.dump(final_data,file,ensure_ascii=False)  
file.close()  
file = open('movie_data.json','r',encoding='utf-8')  
s = json.load(file)  
file.close()  