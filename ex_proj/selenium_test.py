import requests
import json
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('https://movie.douban.com/tag/#/')

def saveMovie(id, name, url):
    with open('douban_movie_list.txt','a') as f:
        line = '%d,%s,%s\n' %(id,name,url)
        f.write(line)

def getAllMovie():
    count = 20
    while True:
        url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=%d' % count
        try:
            r = requests.get(url, timeout=10)
            if r.status_code>=200 and r.status_code<300:
                movies = json.load(r.text)['data']
                if len(movies) == 0:
                    break
                for movie in movies:
                    saveMovie(movie['id'], movie['title'],movie['url'])
                count += 20
        except:
            

getAllMovie()