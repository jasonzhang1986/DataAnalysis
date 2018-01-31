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
headers["Cookie"] = 'bid=JrSvpkFt6Dg; ll="108288"; _vwo_uuid_v2=41493F6119604C9372AFD3AABE4CFD45|36bbf3d6b82026d495c854c1320b4555; __utmc=30149280; ps=y; __utma=30149280.2074300995.1506336189.1517378516.1517396586.11; __utmz=30149280.1517396586.11.7.utmcsr=api.weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/oauth2/authorize; __utmt=1; __utmb=30149280.1.10.1517396586; dbcl2="173350257:0sDMExnpoq4"; ck=xZF9; frodotk="8c770c65861cb2faa5652530925618ee"; push_noty_num=0; push_doumail_num=0'
headers["Host"] = "movie.douban.com"
headers["Referer"] = "http://movie.douban.com/"
headers["Upgrade-Insecure-Requests"] = '1'
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"


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
        time.sleep(60)
        getMovieDetail(line)

def getMovie():
    lineNo = 0
    result_title = ['名字', '导演', '主演', '年份', '时长', '国家', '类型', '评分','评论人数', '五星','四星','三星','二星','一星']
    with open('douban_movie.txt', 'r') as f:
        for line in f.readlines():
            lineNo += 1
            if lineNo==1:
                write_csv(result_title)
                continue
            print('%d %s' %(lineNo, line))
            write_csv(getMovieDetail(line))
            sleep_time = random.randint(1, 5)
            if lineNo%100==0:
                sleep_time = 60
            time.sleep(sleep_time)


getMovie()
