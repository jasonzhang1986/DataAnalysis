import time
import re
import csv
import random
from selenium import webdriver
import os


def write_csv(result):
    with open('douban_movie.csv', 'a', encoding='utf_8_sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)


if not os.path.exists(os.path.join(os.getcwd(), 'douban_movie.csv')):
    write_csv(['名字', '导演', '主演', '年份', '时长', '国家', '类型', '评分','评论人数', '五星','四星','三星','二星','一星'])

browser = webdriver.Chrome()
browser.get('https://movie.douban.com/tag/#/')
browser.implicitly_wait(10)
#获取第一个打开的window的句柄
main_window = browser.current_window_handle
index = 1
try:
    while True:
        #找到第1个电影的item
        elem = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/a[%d]' %index)
        #打印链接
        link = elem.get_attribute('href')
        elem_name = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/a[%d]/p/span[1]' %index)
        name = elem_name.text
        print('index = %d %s %s' % (index, name, link))
        #点击
        elem.click()

        browser.implicitly_wait(3)
        #获取新打开的tab的句柄
        cur_window = browser.window_handles[1]
        #切换
        browser.switch_to.window(cur_window)

        # elem_name = browser.find_element_by_xpath('//*[@id="content"]/h1/span[1]')
        # name = elem_name.text

        elem_info = browser.find_element_by_xpath('//*[@id="info"]')
        # print(elem_info.text)
        info = elem_info.text.split('\n')
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
                actor = item[-1].strip().split('/')[0].strip()
            elif item[0] == '类型':
                category = item[-1].strip()
            elif item[0] == '制片国家/地区':
                district = item[-1].strip()
            elif item[0] == '上映日期':
                showtime = item[-1].strip().split('-')[0]
            elif item[0] == '片长':
                length = item[-1].strip()
                length = re.findall('\d+', length)[0]

        rate = browser.find_element_by_xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong').text
        rate_count = browser.find_element_by_xpath(
            '//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span').text

        rate5 = browser.find_element_by_xpath(
            '//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]').text.split('%')[0]

        rate4 = browser.find_element_by_xpath(
            '//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]').text.split('%')[0]

        rate3 = browser.find_element_by_xpath(
            '//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]').text.split('%')[0]

        rate2 = browser.find_element_by_xpath(
            '//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]').text.split('%')[0]

        rate1 = browser.find_element_by_xpath(
            '//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]').text.split('%')[0]

        # print(type(name))
        # name = name.encode('utf-8')
        # print(name)
        result = [name, director, actor, showtime, length, district, category, rate, rate_count, rate5, rate4, rate3,
                      rate2, rate1]
        print(result)

        write_csv(result)
        time.sleep(random.randint(1, 3))
        browser.close()
        browser.switch_to.window(main_window)
        if index % 20 == 0:
            browser.find_element_by_link_text('加载更多').click()
            time.sleep(random.randint(3,10))
        index += 1


except Exception as e:
    print(e)
finally:
    browser.quit()