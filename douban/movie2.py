import string

import requests
import csv
import re
import json
import time
from bs4 import BeautifulSoup
import random


# USER_AGENT = [
#         'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
#         'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
#         'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
#         'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
#         'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
#         'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
#         'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
#     ]

headers = {}
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers["Accept-Encoding"] = "gzip, deflate, sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2"
# headers["Cache-Control"] = "max-age=0"
headers["Connection"] = "keep-alive"
headers["Host"] = "movie.douban.com"
headers["Referer"] = "http://movie.douban.com/"
headers["Upgrade-Insecure-Requests"] = '1'
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"

# headers = [
#             {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
#             {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
#             {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
#             {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
#             {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
#             {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
#         ]

def write_txt(msg):
    print(msg)
    outputFile = 'douban_movie_2.txt'
    with open(outputFile, 'a',encoding='utf-8') as f:
        f.write(msg)

def getAllMovie():
    # 获取所有标签
    tags = ['爱情','喜剧','科幻','动作','悬疑','犯罪','恐怖','青春','励志','战争','文艺','黑色幽默','传记','情色','暴力','音乐','家庭']

    # headers = {'User-Agent': random.choice(USER_AGENT)}

    print(tags)

    write_txt('id;title;url;rate\n')

    for tag in tags:
        print("Crawl movies with tag: %s" % tag)
        start = 0
        while True:
            if tag=='爱情' and start<5100:
                start = 5100
                continue
            url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%s&start=%d' %(tag,start)
            print('url = ' + url)
            try:
                response = requests.get(url,  headers=headers, timeout=5)
            except Exception as e:
                print(e)
                time.sleep(5)
                continue

            movies = json.loads(response.text)['data']
            if len(movies) == 0:
                break
            for item in movies:
                rate = item['rate']
                title = item['title']
                url = item['url']
                movieId = item['id']
                record = tag + ';' + str(movieId) + ';' + title + ';' + url + ';' + str(rate) + '\n'
                write_txt(record)
                print(tag + '\t' + title)
            start = start + 20
            time.sleep(random.randint(1,3))

def write_csv(result):
    with open('douban_movie.csv', 'a', encoding='gb18030', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)

def verify_ip(proxy, http_type):
    http_url = 'http://www.baidu.com'
    proxy_url = 'http://'+proxy
    has_https = False
    if 'HTTPS' in http_type:
        has_https = True
        proxy_url = 'https://'+proxy

    if has_https:
        proxies={
            'https':proxy_url
        }
    else:
        proxies = {
            'http': proxy_url
        }
    print('proxy_url = %s' %proxies)
    try:
        r = requests.get(http_url, proxies=proxies)
    except Exception as e:
        print('invalid ip',e)
        return False
    else:
        if r.status_code>=200 and r.status_code<300:
            print('IP:%s is Valid' %proxy)
            return True
        else:
            print('IP:%s is Invalid' % proxy)
            return False

def getMovieDetail(line):
    try:
        line = line.split(';')
        movieId = line[0]
        title = line[1]
        url = line[2]
        rate = line[3].rstrip('\n')
        headers = {'User-Agent': random.choice(USER_AGENT)}
        proxies = {
            # 'https': 'https://' + random.choice(proxy)
        }
        response = requests.get(url, headers=headers, proxies=proxies)
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
        time.sleep(3)
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
                sleep_time = 10
            print('sleep %d' % sleep_time)
            time.sleep(sleep_time)


# getMovie()
getAllMovie()