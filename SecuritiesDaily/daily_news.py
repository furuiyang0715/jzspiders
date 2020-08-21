import os
import sys

import requests
from gne import GeneralNewsExtractor
from lxml import html

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)


from base_spider import SpiderBase


class SecuritiesDaily(SpiderBase):
    def __init__(self):
        super(SecuritiesDaily, self).__init__()
        self.list_url = 'http://www.zqrb.cn/stock/zuixinbobao/'
        self.extractor = GeneralNewsExtractor()
        self.list_url_base = 'http://www.zqrb.cn/stock/zuixinbobao/index_p{}.html'
        self.name = '证券日报网-最新播报'
        self.table_name = 'securities_daily_latest'
        self.fields = ['pub_date', 'title', 'type', 'link', 'content']

    def parse_detail(self, link):
        resp = requests.get(link)
        if resp and resp.status_code == 200:
            body = resp.text.encode("ISO-8859-1").decode("utf-8")
            result = self.extractor.extract(body)
            content = result.get("content")
            return content
        else:
            raise Exception("Detail request error.")

    def _create_table(self):
        self._spider_init()
        sql = '''
        CREATE TABLE IF NOT EXISTS `{}`(
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `pub_date` datetime NOT NULL COMMENT '发布时间',
          `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯标题',
          `type` varchar(8) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯类型',
          `link` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯详情页链接',
          `content` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '详情页内容',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `link` (`link`),
          KEY `pub_date` (`pub_date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{}';
        '''.format(self.table_name, self.name)
        self.spider_client.insert(sql)
        self.spider_client.end()

    def start(self):
        self._create_table()
        # for i in range(1, 16):
        for i in range(1, 2):
            list_url = self.list_url_base.format(i)
            resp = requests.get(list_url)
            if resp and resp.status_code == 200:
                body = resp.text.encode("ISO-8859-1").decode("utf-8")
                doc = html.fromstring(body)
                lst = doc.xpath(".//div[@class='news_content']/ul/li")
                items = []
                for li in lst:
                    item = dict()
                    title = li.xpath("./a/@title")[0]
                    try:
                        _type, _title = str(title).split("：", maxsplit=1)
                    except:
                        print("Split Error: {}".format(title))
                        if title:
                            _type = '快讯'
                            _title = title
                        else:
                            raise
                        # raise Exception("Split Error: {}".format(title))
                    link = li.xpath("./a/@href")[0]
                    pub_date = li.xpath("./span[@class='date']")[0].text_content()
                    item['type'] = _type
                    item['title'] = _title
                    item['link'] = link
                    item['pub_date'] = pub_date
                    item['content'] = self.parse_detail(link)
                    print(item)
                    items.append(item)
                self._batch_save(self.spider_client, items, self.table_name, self.fields)


def temp():
    _str = '快讯：10：00民航机场涨3%  7只个股均获超1000万元大单抢筹'
    print(_str.split('：', maxsplit=1))


if __name__ == '__main__':
    # temp()
    SecuritiesDaily().start()
