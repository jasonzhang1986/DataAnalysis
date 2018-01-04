import requests
import json

r = requests.get('http://www.aikustore.com:8080/mjsys/wemall/WemallGoodsAction!list')
# print(r.text)
parsed = r.json()
# print(parsed)
#ensure_ascii=False 避免中文被编码
print(json.dumps(parsed, indent=4, sort_keys=True, ensure_ascii=False))