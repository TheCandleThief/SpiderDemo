# coding: utf-8

"""
爬取知乎回答的部分回答的神回复
"""

from bs4 import BeautifulSoup
import unicodecsv
import requests
from urllib import urlencode
import time
import json
from lxml import html


def get_one(num):
    """
    抓取页面内容
    :param num: 页码标识
    :return: 页面内容 html
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Connection': 'keep-alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/collection/27109279',
        'Cookie': 'tgw_l7_route=69f52e0ac392bb43ffb22fc18a173ee6; _xsrf=668200ce141c1aaf18211a2036e4f22e; _zap=f696bbad-5f2e-4277-a582-b311a6076a3e; d_c0="AADo1s5AVw6PTh_XDTNU2CGWVYfp1Xv9sMk=|1539153628"; q_c1=c47bc85c8eb94681b092930afa3346de|1545269036000|1539153631000; l_n_c=1; r_cap_id="ZmIwNDQ5NjllZTg3NGJmYmIwYjg1NzM5YzQ2N2U1Mzg=|1545269035|73e346ad9178b55019c43292d9853cf2e48a1ccd"; cap_id="MjM1MzI1MjBmMTQ5NDFkOThmYzVmNWEwY2M3MDE0YTM=|1545269035|7e6883a08a28d0ac9bea597031af8a0f656b53f3"; l_cap_id="OTk1ZDZhYjViOGRjNGU2OTg2MWI4OGY3ZGI3NDJlNTU=|1545269035|a1f67261cf288d46272dcf373c9d6ea8efa06167"; n_c=1'
    }
    # params = {
    #     'page': str(num)
    # }
    base_url = 'http://www.zhihu.com/collection/27109279'
    if num == 0:
        url = base_url
    else:
        url = base_url + '?page=' + str(num)  # 生成带参数的url
    print "正在采集：", url   # 抓取带参数的url需要登陆，否则没有访问权限
    try:
        response = requests.get(url, headers=headers)
        print response.status_code
        if response.status_code == 200:
            # print response.text
            return response.text   # 返回抓取页面内容
    except EOFError as e:
        print 111
        print e
        return None


def parse_page(htm):
    """
    解析抓取页面内容
    :param htm: html
    :return: 筛选的有用信息 datas[]
    """
    info = []   # 存储筛选后的有用信息
    soup = BeautifulSoup(htm, "lxml")  # 熬汤
    for d in soup.find_all('div', attrs={"class": "zm-item", "data-type": "Answer"}):
        comic = {}
        comic['title'] = d.find('h2', class_="zm-item-title").find('a').string.strip()

        print comic['title'], '\n' ,"------------"
        info.append(comic)
    return info


def write_to_file(datas):
    """
    将抓取的信息写入文件
    :param datas: 信息列表
    :return: none
    """
    with open('review.csv', 'ab') as f:
        fieldnames = ['Comment', 'User', 'Time']
        writer = unicodecsv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        try:
            for data in datas:
                writer.writerow(data)    # 使用CSV模块，若是中文数据，则会转换为Unicode编码，导致无法写入CSV，故使用UnicodeCSV
            f.close()
        except Exception, e:
            print Exception, ":", e
            pass


# 执行函数
def main():
    for i in range(20):          # 抓取0到19页
        htm = get_one(i)         # 抓取页面内容
        print htm
        datas = parse_page(htm)  # 解析页面
        #write_to_file(datas)     # 将有用信息写入文件
        print "第", i, "页抓取完毕。"
        time.sleep(1)            # 睡眠一秒


if __name__ == '__main__':
    main()

