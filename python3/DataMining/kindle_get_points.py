# -*- coding: utf-8 -*-
"""
Created on Tue May  8 16:27:16 2018

@author: Y
"""

import requests
from bs4 import BeautifulSoup

mail_url = "https://temp-mail.org/"
home_url = 'http://www.yidukindle.com/index.php?from=274335'
regist_url = 'http://www.yidukindle.com/register.php'
headers = {'Referer':home_url}

r = requests.get(mail_url)
r1 = requests.get(home_url)
bs = BeautifulSoup(r.text,'html.parser')
useremail = bs.find("input").attrs["value"]
userpwd = "123456789"
payload = {'useremail': useremail, 'userpwd': userpwd}
r2 = requests.post(regist_url, data=payload,cookies=r1.cookies)