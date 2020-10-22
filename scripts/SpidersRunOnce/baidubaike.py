import multiprocessing
import os
import sys
import time
from functools import wraps

import requests
from bs4 import BeautifulSoup
from base_spider import SpiderBase


class BaiduSpider(SpiderBase):
    """
    爬取百度百科词库
        暂定规则: 请求 http://baike.baidu.com/view/{n}.html  百度会一个词条放一个网页,依次递增, 暂无发现列表接口
    """
    def __init__(self):
        super(BaiduSpider, self).__init__()
        self.base_url = 'http://baike.baidu.com/view/{}.html'
        self.headers.update({"Host": "baike.Baidu.com"})

    def fetch_one(self, i):
        item = dict()
        item['KeyId'] = i
        url = self.base_url.format(i)
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            page = resp.text
            soup = BeautifulSoup(page, features='lxml')
            word = soup.find('h1').get_text()
            try:
                error_info = word.encode("ISO-8859-1").decode("utf-8")
            except:
                item['KeyWord'] = word
                print(item)
                return item
            else:
                print("百度百科错误页")
        else:
            raise


def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('[' + func.__name__ + ']used:' + str(end - start))
        return r
    return wrapper


bd_spider = BaiduSpider()


def task(args):
    for number in range(args[0], args[1]+1):
        bd_spider.fetch_one(number)


@timing
def mul_run():
    mul_count = multiprocessing.cpu_count()
    print("mul count: ", mul_count)
    with multiprocessing.Pool(mul_count) as workers:
        workers.map(task, [(1, 3), (4, 10), (11, 16), (17, 20)])


@timing
def single_run():
    for num in range(1, 21):
        bd_spider.fetch_one(num)


if __name__ == "__main__":
    # single_run()

    mul_run()


    pass
