#-*- encoding: utf-8 -*-
from urllib.request import urlopen,Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from urllib.error import URLError,HTTPError
from time import sleep

def get_moive_name():
    movie_name = []
    for i in range(0,250,25):
        url = 'https://movie.douban.com/top250?start='+str(i)+'&filter='
        bs = BeautifulSoup(urlopen(url),'html.parser')
        movies = bs.find('ol',{'class':'grid_view'})
        for movie in movies.findAll('li'):
            movie_name.append(movie.img.attrs['alt'])
    return movie_name

def search_movie(movie_name = []):
    if len(movie_name) == 0:
        return
    url = 'http://www.80s.tw/search'
    urls = []
    for movie in movie_name:
        print(movie)
        post_data = {'keyword':movie}
        post_data = urlencode(post_data)
        post_data = post_data.encode(encoding='utf_8')
        req = Request(url, post_data)
        try:
            bs = BeautifulSoup(urlopen(req),'html.parser')
        except HTTPError:
            sleep(3)
            bs = BeautifulSoup(urlopen(req),'html.parser')
        try:
            movie_content = bs.find('ul',{'class':'clearfix'}).a
        except Exception:
            u = ''
            urls.append(u)
            continue
        name = movie_content.get_text().strip()
        if movie not in name:
            u = ''
        else:
            u = movie_content.attrs['href']
        if u != '':
            u = 'http://www.80s.tw'+u+'/bd-1'
        urls.append(u)
    return urls

def get_download_link(urls = [],movie_name = []):
    if len(urls) == 0:
        return
    names = []
    links = []
    i = -1
    for url in urls:
        i += 1
        if url == '':
            print(movie_name[i]+'\t找不到该电影')
            names.append(movie_name[i])
            links.append('Null')
            continue
        
        try:
            bs = BeautifulSoup(urlopen(url),'html.parser')
        except URLError:
            url = url.replace('bd-1','hd-1')
            try:
                bs = BeautifulSoup(urlopen(url),'html.parser')
            except Exception:
                print(movie_name[i]+'\t没有标清以上资源')
                names.append(movie_name[i])
                links.append('Null')
                continue
        except Exception:
            print(movie_name[i]+'\t反正就是打不开')
            names.append(movie_name[i])
            links.append('Null')
            continue
            
        name = bs.findAll('a',{'rel':'nofollow'})[0].get_text().strip()
        if name == '高清版':
            name = movie_name[i]
        link = bs.findAll('a',{'rel':'nofollow'})[1].attrs['href']
        print(name,link)
        names.append(name)
        links.append(link)
        
    return names,links

def main():
    movie_name = get_moive_name()
    urls = search_movie(movie_name)
    names,links = get_download_link(urls,movie_name)
    file = open("E:\\links.txt",'w')
    for link in links:
        file.write(link+'\n')
    file.close()
        
if __name__ == '__main__':
    main()
    
    