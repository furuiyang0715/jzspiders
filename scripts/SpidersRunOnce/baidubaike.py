import multiprocessing
import time
from concurrent.futures.thread import ThreadPoolExecutor
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
        self.fields = ['KeyId', 'KeyWord']
        self.table_name = 'baidukeyword'

    def _create_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS `{}` (
          `KeyId` int(11) NOT NULL COMMENT '词条ID',
          `KeyWord` varchar(128) NOT NULL COMMENT '词条',
          UNIQUE KEY `KeyId` (`KeyId`),
          KEY `key_word` (`KeyWord`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='百度词条' ; 
        '''.format(self.table_name)
        self._spider_init()
        self.spider_client.insert(sql)
        self.spider_client.end()

    def bd_save(self, items: list):
        self._spider_init()
        self._batch_save(self.spider_client, items, self.table_name, self.fields)

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
                return item
            else:
                # print("百度百科错误页")
                pass
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
# bd_spider._create_table()


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


def thread_task(args):
    items = []
    start, end = args[0], args[1] + 1
    executor = ThreadPoolExecutor(max_workers=4)
    for item in executor.map(bd_spider.fetch_one, list(range(start, end))):
        if item is not None:
            items.append(item)
    return items


@timing
def mul_run():
    mul_count = multiprocessing.cpu_count()
    print("mul count: ", mul_count)
    combined = []
    with multiprocessing.Pool(mul_count) as workers:
        # result_iter = workers.imap_unordered(task, dispath(1000))
        result_iter = workers.imap_unordered(thread_task, dispath(1000))
        for result_items in result_iter:
            combined.extend(result_items)
            if len(combined) > 50:
                bd_spider.bd_save(combined)
                combined = []
    bd_spider.bd_save(combined)


def dispath(max_number):
    for start in range(max_number // 10 + 1):
        yield start * 10 + 1, start*10 + 10


if __name__ == "__main__":
    # dispath(102)

    # single_run()

    mul_run()   # 目前提速 43个网页/s

    # thread_task((10, 100))

    pass
