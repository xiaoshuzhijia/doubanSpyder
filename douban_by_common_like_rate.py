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
import time

import sys

import pandas as pd
import numpy as np
# 代码出自 https://www.v2ex.com/t/388763
# 似乎是 buffer 写满才输出一次
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    
    def flush(self):
        pass
sys.stdout = Logger("20190521.txt")

s = requests.Session()
url = 'https://accounts.douban.com/j/mobile/login/basic'
#password = input('please input your password:')
data={
    'ck': '',
    'name':'847717213@qq.com',
    'password':'password',
    'remember':'true',
    'ticket': '',
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}
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



def getPageContent(s, url, fileName):
    page = s.get(url)
    with open(fileName, 'w', encoding="utf-8") as f:
        f.write(page.text) #把登陆主页后返回的数据保存到文件中

def getAllContactsFromContactPage(contactPage):
    temp = contactPage.text
    bsObj = BeautifulSoup(temp, features="lxml")
    #bsObj.h1
    div = bsObj.find('ul', {"class":"user-list"}) 
    
    lis = div.findAll("div", {"class":"info"})
    res = []
    # 获取到了 关注人的URL 
    for li in lis:
        print(li.a['href'])
        res.append(li.a['href'])

    return res

def getAllContactsFromContactPageV2(contactPage):
    temp = contactPage.text
    bsObj = BeautifulSoup(temp, features="lxml")

    dds = bsObj.findAll('dd')
    
    res = []
    # 获取到了 关注人的URL 
    for li in dds:
        print(li.a['href'])
        res.append(li.a['href'])

    return res
        
# 从某个ContactPage获取每个关注人的主页
def getAllContactsFromContactPageUrl(contactUrl, s):
    #myContactUrl = 'https://www.douban.com/people/haithink/contacts'
    contactPage = s.get(contactUrl)
    return getAllContactsFromContactPage(contactPage)

def getAllContactsFromContactPageUrlV2(contactUrl, s):
    #myContactUrl = 'https://www.douban.com/people/haithink/contacts'
    contactPage = s.get(contactUrl)
    return getAllContactsFromContactPageV2(contactPage)

# 从主页URL 获取 关注人页面 URL
def getContactPageUrl(homePageUrl):
    if(homePageUrl.endswith("/")):
        return homePageUrl + "contacts"
    else:
         return homePageUrl + "/contacts"

# 从主页URL 获取共同爱好数量
# homePage 是 s.get 得到的对象
def getCommonFromHomePage(homePage):
    pageStr = homePage.text
    idx = pageStr.find('共同的喜好')
    commonLikes = pageStr[idx:idx+10]    
    idx1 = commonLikes.find('(')
    idx2 = commonLikes.find(')')
    if idx1==-1:
        return '0'    
    else:
        return commonLikes[idx1+1:idx2] 
    
    
# 从主页URL 获取已看电影和已看书籍数量
# homePage 是 s.get 得到的对象
def getAllLikeFromHomePage(homePage):
    pageStr = homePage.text
    idx = pageStr.find('部看过')
    if idx!=-1:
        movieLikes = pageStr[idx-10:idx]    
        midx1 = movieLikes.find('>') 
        movieLike = int(movieLikes[midx1+1:])
    else:
        movieLike = 0
    idx = pageStr.find('本读过')
    if idx!=-1:
        bookLikes = pageStr[idx-10:idx]    
        bidx1 = bookLikes.find('>') 
        bookLike = int(bookLikes[bidx1+1:])
    else:
        bookLike = 0
    return movieLike + bookLike
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

    

#接下来是 处理 翻页
# 每页20个， 第2页的URL为 https://www.douban.com/contacts/list?tag=0&start=20
# 这个翻页 还需要研究下， URL 的拼接，可能自己的关注者  和 别人的 关注者 还不一样

#除了从自己的 主页的关注人 开始爬取之外， 在登录之后 可以从 任何 大V的 主页开始爬取
# 需要 考虑到 网络中断、登录退出 等各种意外导致 爬虫 终止的情况， 
# 需要把 所有 爬取过的 主页都记录下来，这样就不用二次 爬取
        
# 可以暂时先不考虑 翻页，只处理第一页 ，也能完成 爬虫的功能

# 那似乎所有功能都有了？
# 从某个人的主页 获取共同爱好数量
        
# first, get all contacts from self home page
# homepage   
#
myPageUrl = 'https://www.douban.com/people/57703328/'

print("-----------")

#print("Going to profile page...")
#homepage = s.get(myPageUrl)
#print(homepage.text)
#with open('my_douban.txt', 'w', encoding="utf-8") as f:
#    f.write(homepage.text) #把登陆主页后返回的数据保存到文件中
    
myContactUrl = getContactPageUrl(myPageUrl)
myContacts = getAllContactsFromContactPageUrl(myContactUrl, s)


def bigLoop(_myContacts, depth = 0):
    if(_myContacts == None):
        return ;
    if(depth == 3):
        return ;
    i=0 
    most_like_rate = np.zeros(shape=(np.size(_myContacts)))
    for contact in  _myContacts:
        print("curr person is ", contact)
        # 先获取某个关注人的共同爱好信息
        contactHomePage = s.get(contact)
        commonLike = getCommonFromHomePage(contactHomePage)       
        AllLike = getAllLikeFromHomePage(contactHomePage) 
        #print("common like is ", commonLike)
        #print("All like is ", str(AllLike))
        #print("common like rate is ", int(commonLike)*1.0/AllLike)
        if AllLike==0:
            most_like_rate[i] = 0
        else:
            most_like_rate[i] = int(commonLike)*1.0/AllLike
        i=i+1
        print(i)
        # 获取 关注人的 关注人列表
        #contackUrl = getContactPageUrl(contact)
        #print("contackUrl: ", contackUrl)
        #contacts = getAllContactsFromContactPageUrlV2(contackUrl, s)
        
        #time.sleep(5)
        #bigLoop(contacts, depth+1)
    print(most_like_rate)
    temp = np.argsort(-most_like_rate)    
    people_score = pd.DataFrame(_myContacts,most_like_rate)
    people_score.to_csv('people_score.csv', mode='a', header=False)
    
    contactsAll = []
    for j in temp[:5]:
        contackUrl = getContactPageUrl(_myContacts[j])
        contacts = getAllContactsFromContactPageUrlV2(contackUrl, s)
        bigLoop(contacts, depth+1)
bigLoop(myContacts, 0)

        



        