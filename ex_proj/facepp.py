import requests
import os
import json
import time
import random
from concurrent.futures import  ThreadPoolExecutor as thpool

api = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
api_key = 'Ayghgsb_3FxSfbZJXLZ7VyiPW4qpbCgu'
api_secret = '5Tag8zWEiC-nD4xUwx1Xww9BC6n8EC3E'
data = {'api_key': api_key, 'api_secret': api_secret, 'return_attributes': 'gender,age'}
files = {}
pic_path = os.path.join(os.getcwd(), 'head')
img_list = os.listdir(pic_path)

count = 0
success_count = 0

# logmsg = ''

def face_detect(img):
    imgpath = os.path.join(pic_path, img)
    files['image_file'] = open(imgpath, 'rb')
    sleep_time = random.random()*3
    time.sleep(sleep_time)
    r = requests.post(api, data, files=files, timeout=5)
    global count
    global success_count
    count = count + 1
    if r.status_code == 200:
        success_count = success_count + 1
        parse_response(img, r.text, sleep_time)
    else:
        print('[%s](sleep_time=%.3f) status_code = %d' % (img, sleep_time, r.status_code))

def copy(src, des):
    src_path = os.path.join(os.getcwd(), 'head', src)
    des_path = os.path.join(os.getcwd(), 'head2', des)
    with open(src_path, 'rb') as f1:
        with open(des_path, 'wb') as f2:
            f2.write(f1.read())


def parse_response(img, text, sleep_time):
    json_dict = json.loads(text)
    attribute = json_dict['faces']
    for attr in attribute:
        time_used = json_dict['time_used']
        age = attr['attributes']['age']['value']
        print('[%s](sleep_time=%.3f) time_used=%dms age=%d' % (img, sleep_time,time_used, age))
        # if age >= 16:
        #     copy(img, img)
        #     global logmsg
        #     logmsg = logmsg + '[%s] time_used=%dms age=%d' % (img, time_used, age) + '\n'



for img in img_list:
    face_detect(img)

# with thpool(max_workers=1) as exe:
#     jobs = []
#     for img in img_list:
#         job = exe.submit(face_detect, img)
#         jobs.append(job)
print('\n')
print('成功率：%.3f  success:%d, count:%d' %(success_count/count, success_count, count))
# print(logmsg)


