# coding: utf-8
# 爬取豆瓣电影排行榜

from bs4 import BeautifulSoup
from lxml import html
import xml
import requests

url = "https://movie.douban.com/chart"  # 豆瓣排行榜
f = requests.get(url)     # get该网页的html内容
soup = BeautifulSoup(f.content, "lxml")  # 用lxml解析器解析网页的内容
# print(f.content)
# print soup.find_all('div', {"class": "pl2"})  # 这是L2

for k in soup.find_all('div', class_="pl2"):   # 找到class是pl2的div标签
    a = k.find_all('span')
    print a[0].string
    print '-----------------------'

