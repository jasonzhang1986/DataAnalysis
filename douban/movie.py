import string

import requests
import csv
import re
import json
import time
from bs4 import BeautifulSoup
import random

headers = {}
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers["Accept-Encoding"] = "gzip, deflate, sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2"
# headers["Cache-Control"] = "max-age=0"
headers["Connection"] = "keep-alive"
headers["Cookie"] = "bid=%s" % ("".join(random.sample(string.ascii_letters + string.digits, 11)))
headers["Host"] = "movie.douban.com"
headers["Referer"] = "http://movie.douban.com/"
headers["Upgrade-Insecure-Requests"] = '1'
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"


user_agent = ['Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
              'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
              'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
              'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
              'Mozilla/5.0 (Android; Tablet; rv:14.0) Gecko/14.0 Firefox/14.0',
              '	Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
              'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
              'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
              'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
              'Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZ054K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
              'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
              'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
              'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',
              'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
              'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
              'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'
              ]

proxies = [
            "61.145.194.26:8080",
            '123.114.206.113:8118',
            '112.251.212.91:8118',
            '183.154.52.48:8118',
            '116.199.115.78:80',
            '118.193.26.18:8080',
            '47.97.176.119:1080',
            '183.163.41.21:45619',
            '58.87.87.142:80',
            '222.169.193.162:8099',
            '116.211.123.138:80',
            '140.143.222.105:1080',
            '120.92.118.127:8080'
          ]

def getAllMovie():
    # 获取所有标签
    tags = []
    url = 'https://movie.douban.com/j/search_tags?type=movie'
    response = requests.get(url,  headers=headers)
    result = json.loads(response.text)
    tags = result['tags']

    print(tags)

    outputFile = 'douban_movie.txt'
    fw = open(outputFile, 'w')
    fw.write('id;title;url;rate\n')

    for tag in tags:
        print("Crawl movies with tag: %s" % tag)
        start = 0
        while True:
            url = "http://movie.douban.com/j/search_subjects?type=movie&tag=%s&page_limit=20&page_start=%d" %(tag,start)
            print('url = ' + url)
            response = requests.get(url,  headers=headers)
            movies = json.loads(response.text)['subjects']
            if len(movies) == 0:
                break
            for item in movies:
                rate = item['rate']
                title = item['title']
                url = item['url']
                movieId = item['id']
                record = str(movieId) + ';' + title + ';' + url + ';' + str(rate) + '\n'
                fw.write(record)
                print(tag + '\t' + title)
            start = start + 20
            time.sleep(3)
    fw.close()

def write_csv(result):
    with open('douban_movie.csv', 'a', encoding='gb18030', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)

def getProxy():
    index = random.randint(0, len(proxies))
    proxy =  {'http': 'http://'+proxies[index]}
    print('proxy='+proxy)
    return proxy

def getHeader():
    index = random.randint(0, len(user_agent))
    headers['User-Agent'] = user_agent[index]
    return headers


def getMovieDetail(line):
    try:
        line = line.split(';')
        movieId = line[0]
        title = line[1]
        url = line[2]
        rate = line[3].rstrip('\n')

        response = requests.get(url, headers=headers)
        html = BeautifulSoup(response.content, 'lxml')
        info = html.select('#info')[0].get_text().split('\n')
        # print(info)
        # print(len(info))
        director = ''
        actor = ''
        category = ''
        district = ''
        showtime = ''
        length = ''
        for item in info:
            item = item.split(':')
            if item[0] == '导演':
                director = item[-1].strip()
            elif item[0] == '主演':
                actor = item[-1].strip()
            elif item[0] == '类型':
                category = item[-1].strip()
            elif item[0] == '制片国家/地区':
                district = item[-1].strip()
            elif item[0] == '上映日期':
                showtime = item[-1].strip()
            elif item[0] == '片长':
                length = item[-1].strip()

        rate_count = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span')[
            0].get_text()

        # interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(1) > span.rating_per
        rate5 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(1) > span.rating_per')[
            0].get_text()
        rate4 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(2) > span.rating_per')[
            0].get_text()
        rate3 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(3) > span.rating_per')[
            0].get_text()
        rate2 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(4) > span.rating_per')[
            0].get_text()
        rate1 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(5) > span.rating_per')[
            0].get_text()

        result = [title, director, actor, showtime, length, district, category, rate, rate_count, rate5, rate4, rate3,
                  rate2, rate1]
        return result
    except:
        print('error!!! %s' % line)
        time.sleep(300)
        getMovieDetail(line)

def getMovie():
    lineNo = 0
    result_title = ['名字', '导演', '主演', '年份', '时长', '国家', '类型', '评分','评论人数', '五星','四星','三星','二星','一星']
    with open('douban_movie.txt', 'r') as f:
        for line in f.readlines():
            lineNo += 1
            if lineNo < 699:
                continue
            if lineNo==1:
                write_csv(result_title)
                continue
            print('%d %s' %(lineNo, line))
            write_csv(getMovieDetail(line))
            sleep_time = random.randint(3, 10)
            if lineNo%100==0:
                sleep_time = 60
            print('sleep %d' % sleep_time)
            time.sleep(sleep_time)


getMovie()
