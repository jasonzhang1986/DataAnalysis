import requests
from lxml import html

r = requests.get('https://movie.douban.com/top250')
tree = html.fromstring(r.text)
#//*[@id="content"]/div/div[1]/ol/li[2]/div/div[2]/div[1]/a/span[1]
#//*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]/text()
titles = tree.xpath('//*[@id="content"]/div/div[1]/ol/*/div/div[2]/div[1]/a/span[1]/text()')
print(titles)
#//*[@id="content"]/div/div[1]/ol/li[6]/div/div[2]/div[2]/p[1]/text()[1]
doctor = tree.xpath('//*[@id="content"]/div/div[1]/ol/*/div/div[2]/div[2]/p[1]/text()[1]')

for d in doctor:
    dd = str(d).strip('\n').strip().split(' ')
    print(dd)

# print(doctor)
