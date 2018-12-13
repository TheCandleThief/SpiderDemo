# coding: utf-8

"""
抓取豆瓣《铁血观音》影评 (抓取10页，保存为CSV文件)
"""
import requests
from urllib import urlencode
import time
from bs4 import BeautifulSoup
import unicodecsv
import json
from lxml import html


def get_one(num):
    """
    抓取页面内容
    :param num: 页码标识
    :return: 页面内容 html
    """
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 66.0.3359.170Safari / 537.36'
    }
    params = {
        'start': str(num),
        'limit': '20',
        'sort': 'new_score',
        'status': 'p',
        'percent_type': ''
    }
    base_url = 'https://movie.douban.com/subject/27113517/comments?'
    if num == 0:
        url = base_url
    else:
        url = base_url + urlencode(params)  # 生成带参数的url
    print "正在采集：", url   # 抓取带参数的url需要登陆，否则没有访问权限
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # print response
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
    for d in soup.find_all('div', class_="comment"):
        comic = {}
        get_infos = d.find_all('span', class_=["comment-info", "short"])

        comic['User'] = get_infos[0].find('a', class_="").string.strip()
        comic['Time'] = get_infos[0].find('span', class_="comment-time").string.strip()
        comic['Comment'] = get_infos[1].string.strip()
        print comic['Comment'], '\n' ,"------------"
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
    for i in range(1):
        htm = get_one(i * 20)    # 抓取页面内容
        datas = parse_page(htm)  # 解析页面
        write_to_file(datas)       # 将有用信息写入文件
        print "本页抓取完毕。"
        time.sleep(1)            # 睡眠一秒


if __name__ == '__main__':
    main()

