import requests
from selenium import webdriver
import os
import time
import mysql.connector

DB_NAME = 'proxy'
Table_Name = 'proxylist_xici'


def update_ip(ip, verifytime):
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('USE %s' % DB_NAME)
    sql = r'update %s SET verifytime = "%s" where ip = "%s"' % (Table_Name, verifytime, ip)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def delte_ip(ip):
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    sql = 'delete from %s where ip = \'%s\'' % (Table_Name, ip)
    print(sql)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def verifyProxyIP(proxy):
    print(proxy)
    url = 'https://www.baidu.com'
    proxies = {
        "http":"http://" + proxy[0] + ":" + proxy[1]
    }
    print(proxies)
    r = requests.get(url, proxies=proxies, timeout=10)
    print(r.status_code)
    if r.status_code==200:
        # print(r.text)
        verifytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        update_ip(proxy[0], verifytime)
    else:
        delte_ip(proxy[0])

def write_db(proxy):
    conn = mysql.connector.connect(user='root', password='password')
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS proxy DEFAULT CHARSET utf8')
    cursor.execute('USE %s' % DB_NAME)
    sql = 'create table IF NOT EXISTS %s (ip varchar(30) NOT NULL, port varchar(10), city varchar(20), type varchar(10), model varchar(10) NOT NULL, usetime varchar(10), verifytime varchar(30));' % Table_Name
    cursor.execute(sql)
    ip = proxy[0]
    sql = 'select * from %s where ip = \'%s\'' % (Table_Name, ip)
    print(sql)
    cursor.execute(sql)
    values = cursor.fetchall()
    if len(values) > 0:
        print('%s exists' %ip)
    else:
        sql = r'insert into %s (ip, port, city, type, model, usetime, verifytime) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (Table_Name, proxy[0], proxy[1], proxy[2], proxy[3], proxy[4],proxy[5], proxy[6])
        print(sql)
        cursor.execute(sql)
    conn.commit()
    conn.close()

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

def fetch_proxy():
    browser = webdriver.Chrome()
    browser.get('http://www.xicidaili.com/nn/')
    browser.implicitly_wait(10)
    #获取第一个打开的window的句柄
    main_window = browser.current_window_handle
    result = []
    page = 20
    while page > 0:
        elems = browser.find_element_by_xpath('//*[@id="ip_list"]/tbody')
        list = elems.text.split('\n')

        # print('list.size = %d' %(len(list)))
        del list[0]
        for i in range(len(list)):
            if i%2 == 0:
                line = list[i] + " " + list[i+1]
                proxy = line.split(' ')
                print(proxy)
                if not 'HTTP' in proxy[4]:
                    page = 0
                    break
                write_db(proxy)
                # result.append(list[i] + " " + list[i+1])


        page -= 1
        # print('page = %d' %page)
        time.sleep(3)
        next_page = browser.find_element_by_link_text('下一页 ›')
        next_page.click()

    browser.quit()

def verify():
    count = getProxyCount()
    for i in range(count):
        proxy = fetchProxyIPFromDb(i)
        verifyProxyIP(proxy)


# fetch_proxy()
verify()
