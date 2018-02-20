import string

import requests
import csv
import re
import json
import time
from bs4 import BeautifulSoup
import random
import pickle
import os
import mysql.connector

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

USER_AGENT = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'
        ]

def write_txt(msg):
    print(msg)
    outputFile = 'douban_movie_2.txt'
    with open(outputFile, 'a',encoding='utf-8') as f:
        f.write(msg)


def write_db(tag, movieid, title, directors, actors, rate, star, cover):
    title = title.replace(r'"', '')
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS douban DEFAULT CHARSET utf8')
    cursor.execute('USE douban')
    sql = 'create table IF NOT EXISTS movielist (movieid int(11) NOT NULL, tag varchar(10), title varchar(100) NOT NULL, directors varchar(200), actors varchar(200), rate varchar(10), star int(2), cover varchar(200));'
    cursor.execute(sql)

    sql = 'select * from movielist where movieid = \'%s\'' %movieid
    print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    if len(values) > 0:
        return

    sql = r'insert into movielist (movieid, tag, title, directors, actors, rate, star, cover) values ("%d", "%s", "%s", "%s", "%s", "%s", "%d", "%s")' % (
    int(movieid), tag, title, directors, actors, rate, int(star), cover)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def load_tmp():
    d = {'tag':'剧情', 'index':0}
    try:
        with open(os.path.join(os.getcwd(), 'temp.txt'), 'rb') as f:
            d = pickle.load(f)
    except Exception as e:
        print(e)
    return d

def save_tmp(tag, index):
    a = {"tag": tag, "index": index}
    with open('temp.txt', 'wb') as f:
        pickle.dump(a, f)

def load_db_lineNo():
    d = {'lineNo':0}
    try:
        with open(os.path.join(os.getcwd(), 'lineNo.txt'), 'rb') as f:
            d = pickle.load(f)
    except Exception as e:
        print(e)
    return d

def save_db_lineNo(lineNo):
    a = {'lineNo':lineNo}
    with open('lineNo.txt', 'wb') as f:
        pickle.dump(a, f)

def getAllMovie():
    # 获取所有标签
    tags = ['剧情','爱情','喜剧','科幻','动作','悬疑','犯罪','恐怖','青春','励志','战争','文艺','黑色幽默','传记','情色','暴力','音乐','家庭']

    # headers = {'User-Agent': random.choice(USER_AGENT)}

    print(tags)

    retry = True

    write_txt('id;title;url;rate\n')

    retry_count = 20
    for tag in tags:
        print("Crawl movies with tag: %s" % tag)
        start = 0
        while True:
            if retry:
                d = load_tmp()
                print(d)
                if tags.index(tag) < tags.index(d['tag']):
                    break
                elif tag == d['tag'] and start<d['index']:
                    start = d['index']
            retry = False
            save_tmp(tag, start)

            url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%s&start=%d' %(tag,start)
            print('url = ' + url)
            try:
                response = requests.get(url,  headers=headers, timeout=5)
                movies = json.loads(response.text)['data']
            except Exception as e:
                retry_count = retry_count-1
                if retry_count == 0:
                    return
                print(e)
                time.sleep(5)
                continue

            retry_count = 20
            if len(movies) == 0:
                break
            for item in movies:
                print(item)
                rate = item['rate']
                title = item['title']
                url = item['url']
                movieId = item['id']
                star = item['star']
                directors = item['directors']
                cover = item['cover']
                if directors and len(directors)>0:
                    directors = ','.join(directors)
                    if len(directors) > 200:
                        directors = directors[:200]
                else:
                    directors=''
                directors = directors.replace(r'"', r"'")

                actors = item['casts']
                if actors and len(actors)>0:
                    actors = ','.join(actors)
                    if len(actors) > 200:
                        actors = actors[:200]
                else:
                    actors = ''
                actors = actors.replace(r'"', r"'")

                # record = [title, movieId, url, rate, star]
                # getDetail(record)
                line = tag + ';' + str(movieId) + ';' + title + ';' + url + ';' + str(rate) + ";" + str(star) + ';' + directors + ';' + actors
                print(line)
                # record = getMovieDetail(line)
                # write_csv(record)
                write_db(tag, movieId, title, directors, actors, rate, star, cover)
                # write_txt(record)
                # print(tag + '\t' + title)
            start = start + 20
            time.sleep(random.randint(1,3))

def write_csv(result):
    with open('douban_movie_22.csv', 'a', encoding='utf_8_sig', newline='') as csvfile:
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
        tag = line[0]
        movieId = line[1]
        title = line[2]
        url = line[3]
        rate = line[4]
        star = line[5].rstrip('\n')
        # headers = {'User-Agent': random.choice(USER_AGENT)}
        proxies = {
            # 'https': 'https://' + random.choice(proxy)
        }
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
                showtime = item[-1].strip().split('-')[0]
            elif item[0] == '片长':
                length = item[-1].strip()
                length = re.findall('\d+', length)[0]

        rate_count = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span')[
            0].get_text()

        # interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(1) > span.rating_per
        rate5 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(1) > span.rating_per')[
            0].get_text().split('%')[0]
        rate4 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(2) > span.rating_per')[
            0].get_text().split('%')[0]
        rate3 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(3) > span.rating_per')[
            0].get_text().split('%')[0]
        rate2 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(4) > span.rating_per')[
            0].get_text().split('%')[0]
        rate1 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(5) > span.rating_per')[
            0].get_text().split('%')[0]

        result = [tag, movieId, title, director, actor, showtime, length, district, category, star, rate, rate_count, rate5, rate4, rate3,
                  rate2, rate1]
        print(result)
        return result
    except:
        print('error!!! %s' % line)
        time.sleep(3)
        getMovieDetail(line)


def fetchProxyIPFromDb(lineNo):
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE proxy')

    sql = r'select * from proxylist limit %d,1' % (lineNo)
    print(sql)
    cursor.execute(sql)
    proxy = cursor.fetchone()
    conn.commit()
    conn.close()
    return proxy

def getProxyCount():
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE proxy')

    sql = r'select count(*) from proxylist'
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0]

retry_count = 20
def getMovieDetail2(movie):
    print('getMovieDetail ', movie)
    global retry_count
    try:
        movieid = movie[0]
        tag = movie[1]
        title = movie[2]
        director = movie[3]
        actor = movie[4]
        rate = movie[5]
        star = movie[6]
        cover = movie[7]
        url = 'https://movie.douban.com/subject/%d/' %movieid
        proxy_count = getProxyCount()
        # headers['User-Agent'] = random.choice(USER_AGENT)
        proxy_ip = fetchProxyIPFromDb(random.randint(0,proxy_count-1))[0]
        proxies = {
            "http": "http://" + proxy_ip
        }
        print(headers)
        print(proxies)
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        print('response code = ', response.status_code)
        # print(response.text)
        if response.status_code >=200 and response.status_code<300:
            html = BeautifulSoup(response.content, 'lxml')
            # print(html.select('#body'))
            # body = html.select('body')[0].get_text();
            if '检测到有异常请求从你的 IP 发出' in response.text:
                print("检测到有异常请求从你的 IP 发出", response.text)
                return [0]
            if '<script>var d=[navigator.platform,navigator.userAgent,navigator.vendor].join("|");window.location.href="https://sec.douban.com/a?' in response.text:
                print("检测到有异常请求从你的 IP 发出", response.text)
                return [0]
            # print(html)
            info = html.select('#info')
            if len(info) == 0:
                print(response.text)
                return [-2]
            info = html.select('#info')[0].get_text().split('\n')
            print(info)
            # print(len(info))
            category = ''
            district = ''
            showtime = ''
            length = ''
            for item in info:
                item = item.split(':')
                if item[0] == '类型':
                    category = item[-1].strip()
                elif item[0] == '制片国家/地区':
                    district = item[-1].strip()
                elif item[0] == '上映日期':
                    showtime = item[-1].strip().split('-')[0]
                elif item[0] == '片长':
                    length = item[-1].strip()
                    length = re.findall('\d+', length)[0]

            category = category.replace(r'/',',')
            if len(district) > 0:
                district = district[:50]

            if len(category) > 0:
                category = category[:30]
            rate_count = html.select(
                '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span')[
                0].get_text()

            # interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(1) > span.rating_per
            rate5 = html.select(
                '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(1) > span.rating_per')[
                0].get_text().split('%')[0]
            rate4 = html.select(
                '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(2) > span.rating_per')[
                0].get_text().split('%')[0]
            rate3 = html.select(
                '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(3) > span.rating_per')[
                0].get_text().split('%')[0]
            rate2 = html.select(
                '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(4) > span.rating_per')[
                0].get_text().split('%')[0]
            rate1 = html.select(
                '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(5) > span.rating_per')[
                0].get_text().split('%')[0]

            result = [movieid, tag, title, director, actor, showtime, length, district, category, star, rate, int(rate_count), rate5, rate4, rate3,
                      rate2, rate1, cover]
            print(result)
            return result
        else:
            return [-1]
    except Exception as e:
        # print('error!!! %s' % movie)
        # print('exception 1')
        print(e, movie[0],movie[2])
        return None

def getMovie():
    lineNo = 0
    result_title = ['名字', '导演', '主演', '年份', '时长', '国家', '类型', '评分','评论人数', '五星','四星','三星','二星','一星']
    with open('douban_movie_2.txt', 'r') as f:
        for line in f.readlines():
            lineNo += 1
            # if lineNo < 699:
            #     continue
            if lineNo==1:
                write_csv(result_title)
                continue
            print('%d %s' %(lineNo, line))
            write_csv(getMovieDetail(line))
            sleep_time = random.randint(1, 3)
            if lineNo%500==0:
                sleep_time = 10
            print('sleep %d' % sleep_time)
            time.sleep(sleep_time)


def getMovieFromDb(lineNo):
    movie = None
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE douban')

    sql = r'select * from movielist limit %d,1' %lineNo
    print(sql)
    cursor.execute(sql)
    movie = cursor.fetchone()
    conn.commit()
    conn.close()
    return movie

def getMovieCount():
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE douban')

    sql = r'select count(*) from movielist'
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0]

def saveMovieDetail(movie):
    print(movie)
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS douban DEFAULT CHARSET utf8')
    cursor.execute('USE douban')
    #movieid,tag, title, director, actor, showtime, length, district, category, star, rate, rate_count, rate5, rate4, rate3,rate2, rate1
    sql = 'create table IF NOT EXISTS moviedetail (movieid int(11) NOT NULL, tag varchar(10), title varchar(100) NOT NULL, directors varchar(200), actors varchar(200), showtime varchar(20), length varchar(5), district varchar(50), category varchar(30), star int(2), rate varchar(10), rate_count int(12), rate5 varchar(6), rate4 varchar(6), rate3 varchar(6), rate2 varchar(6), rate1 varchar(6), cover varchar(200));'
    cursor.execute(sql)

    sql = 'select * from moviedetail where movieid = \'%d\'' % movie[0]
    print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    if len(values) > 0:
        print("alread exists %d" %movie[0])
        return
    sql = r'insert into moviedetail (movieid, tag, title, directors, actors, showtime, length, district, category, star, rate, rate_count, rate5, rate4, rate3, rate2, rate1, cover) values ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s")' % (
        movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6],movie[7], movie[8],movie[9],movie[10],movie[11],movie[12],movie[13],movie[14],movie[15],movie[16],movie[17])
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def getMovies():
    movie_count = getMovieCount()
    lineNo = load_db_lineNo()['lineNo']
    print('lineNo = %d' %lineNo)
    while lineNo < movie_count:
        retry_count = 20
        movie = getMovieFromDb(lineNo)
        movie_detail = None
        while retry_count > 0:
            retry_count -= 1
            movie_detail = getMovieDetail2(movie)
            print('---', movie_detail)
            if movie_detail:
                if len(movie_detail) > 1:
                    saveMovieDetail(movie_detail)
                elif movie_detail[0]==0:
                    print('ip 被封了')
                    return
                break
            else:
                time.sleep(random.randint(1, 3))

        if movie_detail is None:
            return

        lineNo += 1
        save_db_lineNo(lineNo)


# getMovie()
# getAllMovie()
# save_db_lineNo(8800)
getMovies()