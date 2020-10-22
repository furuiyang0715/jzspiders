import os
import sys
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
                return item
            else:
                print("百度百科错误页")
        else:
            raise


def slice(mink, maxk):
    s = 0.0
    for k in range(int(mink), int(maxk)):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def main(n):
    pids = []
    unit = n // 10
    print("单个子进程分配的计算量是 {}".format(unit))

    for i in range(10):
        mink = unit * i
        maxk = mink + unit
        print("单个进程处理的起止点是从 {} 到 {}".format(mink, maxk))
        pid = os.fork()
        if pid > 0:
            pids.append(pid)
        else:
            slice(mink, maxk)
            sys.exit(0)

    # TODO

    for pid in pids:
        os.waitpid(pid, 0)  # 等待子进程结束


if __name__ == "__main__":
    # test single spider
    # bd = BaiduSpider()
    # print(bd.fetch_one(666))
    # print(bd.fetch_one(10000000))

    main(1000000)
