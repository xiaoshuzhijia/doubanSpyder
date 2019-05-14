# -*- coding: utf-8 -*-
"""
Created on Wed May  8 20:29:27 2019
spyder test
@author: haithink
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("https://www.pythonscraping.com/pages/warandpeace.html")
#html = urlopen("https://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, features="lxml")

#print(bsObj.h1)

#nameList = bsObj.findAll("span", {"class":"green"})
#for name in nameList:
#    print(name.get_text)
    
allText = bsObj.findAll(id="text")
print(allText[0].attrs)    

#for child in bsObj.find("table", {"id":"giftList"}).children:
#    print(child)