#-*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
from urllib import request
from urllib.parse import urlencode
from time import sleep

#该地址是你提交问卷的目标地址，具体在浏览器内自行测试
url = 'https://sojump.com/handler/processjq.ashx?submittype=1&curID=13930071&t=1494382443451&starttime=2017%2F5%2F10%2010%3A13%3A53&rn=1779472485.29857501&sd=http%3a%2f%2fwww.sojump.com%2f'


i = 0
while True:
    #该处可以按照自己的需要生成随机数
    data = '1$1}2$2}3$2}4$2}5$'
    post_data = {'submitdata':data}
    post_data = urlencode(post_data)
    post_data = post_data.encode(encoding='utf_8')
    #使用自己安装好的Opener
    response = request.urlopen(url,post_data)
    #读取相应信息并解码
    html = response.read().decode("utf-8")
    print(data,i+1)
    #成功的话会出现一串字符，末尾数字表示当前完成的总份数   
    print(html)
    i = i+1
    if i%3 == 0:
        #此处是为了防止同一IP地址提交太频繁需要输入验证码
        sleep(60)
    
