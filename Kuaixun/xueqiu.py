import json
import time

import requests


class XueQiuKuaiXun(object):
    def __init__(self):
        self.web_url = 'https://xueqiu.com/today#/livenews'
        self.first_api = 'https://xueqiu.com/statuses/livenews/list.json?since_id=-1&max_id=-1&count=10'
        self.base_api = 'https://xueqiu.com/statuses/livenews/list.json?since_id=-1&max_id={}&count=15'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            'Cookie': 's=dk1af2e0xx; device_id=225b7001f44831dd2c0ef9a0a27c309c; __utma=1.390898764.1595042617.1595042617.1595042617.1; __utmz=1.1595042617.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAADZ1qkEJjAIA4U5tcaMBWxG5jhDi; xq_a_token=4db837b914fc72624d814986f5b37e2a3d9e9944; xqat=4db837b914fc72624d814986f5b37e2a3d9e9944; xq_r_token=2d6d6cc8e57501dfe571d2881cabc6a5f2542bf8; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYwMDQ4MzAwNywiY3RtIjoxNTk3OTE1NjU0NjMzLCJjaWQiOiJkOWQwbjRBWnVwIn0.Xv18aNMnTCbBSBdBeEBlebGCJRVna9F89ghYs2iTc2zXztEJJ6az2lWMX7E78Nt1aVY97kPhNMs0IcCtHWX7WOX3xqZMUQpUi_ZbDTv7vUoOIBKB27jtenSkM6i_u3pgDrVvyXngbcnof-zKv86LzfcgQSCL3GcnmtwHFmoXctumpD8Z400r3m753u7uNnFOptyGJaIDIqvcF6vlBjm01b18WwYrkjIcW3ujJPGkTr38O9FYujILUQjCdRQZsTgEQfK3bPWeOJNFd8V9rMXl0tZlYN7m1yhL1DYeMqyTvCY5rvkzUQ6cWyBJJZ615auqmflzwe__i-reu-6D_6U53w; u=561597915688189; Hm_lvt_1db88642e346389874251b5a1eded6e3=1597915690,1597990683; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1597990683',
        }

    def fetch_datas(self, url):
        resp = requests.get(url, headers=self.headers)
        if resp and resp.status_code == 200:
            text = resp.text
            datas = json.loads(text)
            # next_id = datas.get("next_id")
            next_max_id = datas.get("next_max_id")
            next_url = self.base_api.format(next_max_id)
            items = datas.get("items")
            for item in items:
                print(item)
            return next_url

    def start(self):
        next_url = self.fetch_datas(self.first_api)
        print("next: ", next_url)
        time.sleep(5)
        self.fetch_datas(next_url)


if __name__ == '__main__':
    XueQiuKuaiXun().start()
