import pickle
import random
import string
import time
from PIL import Image
import os
import base64
import json
import requests
import logging.handlers
import datetime
import logging


def get_code(driver, id):
    #获取验证码图片
    t = time.time()
    path = os.path.dirname(os.path.dirname(__file__)) + '\\screenshots'
    picture_name1 = path + '\\' + str(t) + '.png'

    driver.save_screenshot(picture_name1)

    ce = driver.find_element_by_id(id)

    left = ce.location['x']
    top = ce.location['y']
    right = ce.size['width'] + left
    height = ce.size['height'] + top

    fbl = driver.execute_script('return window.devicePixelRatio')

    im = Image.open(picture_name1)
    img = im.crop((left * fbl, top * fbl, right * fbl, height * fbl))

    t = time.time()
    picture_name2 = path + '\\' + str(t) + '.png'
    img.save(picture_name2)

    with open(picture_name2, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": 'ry', "password": '158666Ry', "typeid": 3, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""

#随机生成字符串
def gen_random_str():
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    return ran_str


def get_logger():
    path = os.path.dirname(os.path.dirname(__file__)) + '\\logs'
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    rf_handler = logging.handlers.TimedRotatingFileHandler(path + '\\'+'all.log', when='midnight', interval=1, backupCount=7,
                                                           atTime=datetime.time(0, 0, 0, 0), encoding="utf-8")
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

    f_handler = logging.FileHandler(path + '\\'+'error.log', encoding="utf-8")
    f_handler.setLevel(logging.ERROR)
    f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    return logger

def save_cookie(driver, path):
    pass

def load_cookie(driver, path):
    pass