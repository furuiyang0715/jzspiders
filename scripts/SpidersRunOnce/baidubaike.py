import multiprocessing
import time
from functools import wraps

import requests
from bs4 import BeautifulSoup
from base_spider import SpiderBase


class BaiduSpider(SpiderBase):
    """
    需求: 爬取百度百科词库
        暂定规则: 请求 http://baike.baidu.com/view/{n}.html  百度会一个词条放一个网页,依次递增, 暂无发现列表接口
        目前词库更新到 4,000, 000 左右
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


# @timing
# def single_run():
#     for num in range(1, 21):
#         bd_spider.fetch_one(num)


def task(args):
    items = []
    for number in range(args[0], args[1]+1):
        item = bd_spider.fetch_one(number)
        if item is not None:
            items.append(item)
    return items


@timing
def mul_run():
    mul_count = multiprocessing.cpu_count()
    print("mul count: ", mul_count)
    combined = []
    with multiprocessing.Pool(mul_count) as workers:
        # workers.map(task, [(1, 3), (4, 10), (11, 16), (17, 20)])
        result_iter = workers.imap_unordered(task, [(1, 3), (4, 10), (11, 16), (17, 20)])
        for result_items in result_iter:
            combined.extend(result_items)
    print(combined)


if __name__ == "__main__":
    # single_run()

    mul_run()


    pass
