### 要求：通过 requests 请求， 通过 lxml 的 xpath 方式解析字段，并将结果保存到 excel 中。

不多说直接 show the code

```python
import requests
from lxml import html
import re
import csv

#解析html网页
def parse_tree(url):
    r = requests.get(url)
    tree = html.fromstring(r.text)
    return tree
```


```python
#获取title
def get_title(tree):
    titles = tree.xpath('//*[@id="content"]/div/div[1]/ol/*/div/div[2]/div[1]/a/span[1]/text()')
    arr_title = []
    # print(titles)
    for title in titles:
        arr_title.append(str(title))
#     print(arr_title)
    return arr_title
```


```python
#获取导演和主演，只取第一个名字
def get_da(tree):
    doctor = tree.xpath('//*[@id="content"]/div/div[1]/ol/*/div/div[2]/div[2]/p[1]/text()[1]')
    da = []
    for d in doctor:
#         print(d)
        dd = re.split(r'[\s\\xa0]', str(d))
#         print(dd)
        dactor = ''
        actor = ''
        for s in dd:
            if '导演' in s:
                index1 = dd.index(s)
                if index1+1 < len(dd):
                    dactor = dd[index1+1]
            elif '主演' in s:
                index = dd.index(s)
                if index+1 < len(dd):
                    actor = dd[index+1]
                break
        arr = [dactor, actor]
        da.append(arr)
#     print(da)
    return da
```


```python
#获取年份
def get_years(tree):
    years = tree.xpath('//*[@id="content"]/div/div[1]/ol/*/div/div[2]/div[2]/p[1]/text()[2]')
    arr_year = []
    for y in years:
        year = str(y).strip('\n').strip().split('\xa0/\xa0')
        arr_year.append(year)
#     print(arr_year)
    return arr_year
```


```python
#获取评分
def get_rate(tree):
    rates = tree.xpath('//*[@id="content"]/div/div[1]/ol/*/div/div[2]/div[2]/div/span[2]/text()')
    arr_rate = []
    # print(rates)
    for r in rates:
        arr_rate.append(str(r))
#     print(arr_rate)
    return arr_rate
```


```python
#将结果拼接到result中
def append(result,arr_title, arr_da, arr_year, arr_rate):
    for i in range(len(arr_title)):
        a = (arr_title[i], arr_da[i][0],arr_da[i][1], arr_year[i][0],arr_year[i][1],arr_year[i][2], arr_rate[i])
        result.append(a)


```


```python
result_title = ['名字', '导演', '主演', '年份', '国家', '类型', '评分']
result = []

for i in range(10): #一共10页
    count = i * 25 #每页25条数据
    url = 'https://movie.douban.com/top250?start=%d' %(count) #拼接每页的url地址
    print(url)
    tree = parse_tree(url) #解析html
    #拼接数据到result中
    append(result,get_title(tree), get_da(tree), get_years(tree), get_rate(tree))

#输出一下看看结果
print(result_title)
for r in result:
    print(r)

#保存到csv中， newline字段是设置换行，默认是'\n'，会直接在csv中插入空行
csvfile = open('douban_top250.csv', 'w', encoding='gb18030', newline='')
writer = csv.writer(csvfile)
#先写入title
writer.writerow(result_title)
print('====================')
for r in result:
    print(r)
    #写入每一条数据，如果出错则跳过该条数据
    try:
        writer.writerow(r)
    except:
        continue
csvfile.close() #最后关闭文件
```

好了，是不是很简单，我们来看一下结果

![img](douban_top250.png)

so Easy 吧！
