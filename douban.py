# -*- coding: utf-8 -*-
"""
Created on Thu May  9 19:50:23 2019
douban scrape
@author: haithink
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen

import requests
import os

s = requests.Session()
url = 'https://accounts.douban.com/j/mobile/login/basic'
password = input('please input your password:')
data={
    'ck': '',
    'name':'haithink@gmail.com',
    'password':password,
    'remember':'true',
    'ticket': '',
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
r = s.post(url, data, headers=headers)


html = r.json()
if html['status'] == 'success':
    print('登录成功')
else:
    print('登录失败')
    print('验证码路径',html['payload']['captcha_image_url'])
    captcha = input('please input the captcha:')
    data['captcha-solution'] = captcha
    data['captcha-id'] = html['payload']['captcha_id']
    r = s.post(url, data, headers=headers)

    #os._exit(0)
print(r.text)
print("Cookie is set to:")
print(s.cookies.get_dict())
#
myPage = 'https://www.douban.com/people/haithink/'

print("-----------")
print("Going to profile page...")
homepage = s.get(myPage)
#print(homepage.text)

with open('my_douban.txt', 'w') as f:
    f.write(homepage.text) #把登陆主页后返回的数据保存到文件中

def getPageContent(s, url, fileName):
    page = s.get(url)
    with open(fileName, 'w', encoding="utf-8") as f:
        f.write(page.text) #把登陆主页后返回的数据保存到文件中

# 这个是获取自己关注的人        
#contactListUrl = 'https://www.douban.com/people/haithink/contacts'    
#getPageContent(s, contactListUrl, 'doubancontactList.txt')

#movieUrl = 'https://www.douban.com/note/705736195/'
#getPageContent(s, movieUrl, 'note.txt')

# 在已经登录的情况下，访问某个人的主页，可以看到 他 和自己的共同爱好
#testPerson = 'https://www.douban.com/people/79769824/'
#getPageContent(s, testPerson, '79769824.txt')

# 在已经登录的情况下，如下链接获取 他 关注的人
# https://www.douban.com/people/79769824/contacts

# 在已经登录的情况下，如下链接获取 关注他的人
# https://www.douban.com/people/79769824/rev_contacts

# 先假设， 每个人 的关注人页面 URL， 以及 关注他的人页面 URL 都是 写死的，除了 那个前缀

# 然后，需要一个函数，从 某个链接获取 所有的关注人，输入为某个页面的URL 或者 页面文本

# 另一个函数， 获取 关注他的人 ，输入为某个页面的URL 或者 页面文本

#myContactUrl = 'https://www.douban.com/people/haithink/contacts'
#myContactPage = s.get(myContactUrl)
#temp = myContactPage.text
#bsObj = BeautifulSoup(temp, features="lxml")
#bsObj.h1
#div = bsObj.find('ul', {"class":"user-list"})

#lis = div.findAll("div", {"class":"info"})
# 获取到了 关注人的URL 
# lis[0].a['href']
#for li in lis:
#    print(li.a['href'])        

#接下来是 处理 翻页
# 每页20个， 第2页的URL为 https://www.douban.com/contacts/list?tag=0&start=20
# 这个翻页 还需要研究下， URL 的拼接，可能自己的关注者  和 别人的 关注者 还不一样

#除了从自己的 主页的关注人 开始爬取之外， 在登录之后 可以从 任何 大V的 主页开始爬取
# 需要 考虑到 网络中断、登录退出 等各种意外导致 爬虫 终止的情况， 
# 需要把 所有 爬取过的 主页都记录下来，这样就不用二次 爬取
        
        
        
        



        