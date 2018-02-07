import requests
import csv
import json
import time

url = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid=862000610313200287&num=20&result_fields=1,2,3&result_format=json'


def fetch():
    response = requests.get(url, timeout=10)
    result = json.loads(response.text)
    proxy = result['result']
    return proxy

def save(result):
    with open('proxy.csv','a', newline='') as csv_file:
        writer = csv.writer(csv_file)
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



# count = 5000
# while count >=0:
#     count -= 1
#     data = fetch()
#     for proxy in data:
#         r = [proxy['ip:port'], proxy['http_type']]
#         if verify_ip(proxy['ip:port'],proxy['http_type']):
#             save(r)
#     time.sleep(2)


with open('proxy.csv','r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        proxy = row[0]
        data = proxy.split(',')
        # print(data)
        verify_ip(data[0], data[1])
        with open('proxy1.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
        # print('%s %s' %(row[0], row[1]))
        # print(len(row))
        # print('\n'.join(row))