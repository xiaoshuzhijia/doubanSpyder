# -*- coding: utf-8 -*-
"""
Created on Thu May  9 20:43:31 2019

@author: haithink
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen

import requests

url = 'https://accounts.douban.com/j/mobile/login/basic'
data={
    'ck': '',
    'name':'haithink@gmail.com',
    'password':'yourpassword',
    'remember':'true',
    'ticket': '',
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
r = requests.post(url, data, headers=headers)

print(r.text)