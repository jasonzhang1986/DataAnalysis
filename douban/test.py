import requests
import json
import mysql.connector
import time
import random


proxy_url = 'http://lab.crossincode.com/proxy/get/'
proxy_url_https = 'http://lab.crossincode.com/proxy/get/?head=https'
DB_NAME = 'proxy'
Table_Name = 'proxylist'

def write_db(ip, type, model, verifytime):
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS proxy DEFAULT CHARSET utf8')
    cursor.execute('USE %s' % DB_NAME)
    sql = 'create table IF NOT EXISTS %s (ip varchar(30) NOT NULL, type varchar(10), model varchar(10) NOT NULL, verifytime varchar(30));' % Table_Name
    cursor.execute(sql)

    sql = 'select * from %s where ip = \'%s\'' % (Table_Name, ip)
    print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    if len(values) > 0:
        print('%s exists' %ip)
        sql = r'update %s SET verifytime = "%s"'% (Table_Name, verifytime)
    else:
        sql = r'insert into %s (ip, type, model, verifytime) values ("%s", "%s", "%s", "%s")' % (Table_Name, ip, type, model, verifytime)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def fetchProxy(https=False):
    url = proxy_url
    type = 'http'
    if https:
        url = proxy_url_https
        type = 'https'
    r = requests.get(url)
    if r.status_code >= 200 and r.status_code < 300:
        proxies = json.loads(r.text)['proxies']
        for proxy in proxies:
            # verifytime = time.mktime(time.strptime(proxy['最后验证时间'],'%Y-%m-%d %H:%M:%S'))
            write_db(proxy[type], type, proxy['类型'], proxy['最后验证时间'])

def fetchProxyIPFromDb(lineNo):
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE %s' % DB_NAME)

    sql = r'select * from %s limit %d,1' % (Table_Name,lineNo)
    print(sql)
    cursor.execute(sql)
    proxy = cursor.fetchone()
    conn.commit()
    conn.close()
    return proxy

def getProxyCount():
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE %s' % DB_NAME)

    sql = r'select count(*) from %s' % Table_Name
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return result[0]

def verifyProxyIP(ip, type):
    print(ip, type)
    url = 'http://www.baidu.com/'
    proxies = {
        "http":"http://" + ip,
        "https":"http://" + ip
    }
    print(proxies)
    r = requests.get(url, proxies=proxies)
    print(r.status_code)
    if r.status_code==200:
        verifytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        write_db(ip, type, '高匿', verifytime)

fetchProxy()
count = getProxyCount()
proxy = fetchProxyIPFromDb(random.randint(1,count-1))
verifyProxyIP(proxy[0], proxy[1])