import os
import sys

import requests
from gne import GeneralNewsExtractor
from lxml import html

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)


from base_spider import SpiderBase
from scripts import utils


class SecuritiesDaily(SpiderBase):
    def __init__(self):
        super(SecuritiesDaily, self).__init__()
        self.list_url = 'http://www.zqrb.cn/stock/zuixinbobao/'
        self.extractor = GeneralNewsExtractor()
        self.list_url_base = 'http://www.zqrb.cn/stock/zuixinbobao/index_p{}.html'
        self.table_name = 'securities_daily_latest'
        # self.name = '证券日报网-最新播报'
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]
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

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def run(self):
        self._spider_init()
        for i in range(1, 2):
            list_url = self.list_url_base.format(i)
            resp = requests.get(list_url)
            if resp and resp.status_code == 200:
                body = resp.text.encode("ISO-8859-1").decode("utf-8")
                doc = html.fromstring(body)
                lst = doc.xpath(".//div[@class='news_content']/ul/li")
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
                    link = li.xpath("./a/@href")[0]
                    pub_date = li.xpath("./span[@class='date']")[0].text_content()
                    item['InnerType'] = _type
                    item['Title'] = _title
                    item['Website'] = link
                    item['PubDatetime'] = pub_date
                    item['Content'] = self.parse_detail(link)
                    # 增加汇总表字段
                    item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                    item['MedName'] = self.name
                    item['OrgMedName'] = self.name
                    item['OrgTableCode'] = self.table_code
                    print(item)
                    self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
title as Title,\
link as Website,\
type as InnerType, \
content as Content, \
CREATETIMEJZ as CreateTime, \
UPDATETIMEJZ as UpdateTime \
from {} limit {}, 1000; '''.format(self.table_name, i*1000)
            datas = self.spider_client.select_all(trans_sql)
            print(len(datas))
            if not datas:
                break
            for data in datas:
                data['DupField'] = "{}_{}".format(self.table_code, data['Website'])
                data['MedName'] = self.name
                data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


def temp():
    _str = '快讯：10：00民航机场涨3%  7只个股均获超1000万元大单抢筹'
    print(_str.split('：', maxsplit=1))


if __name__ == '__main__':
    # temp()

    # SecuritiesDaily().start()

    # SecuritiesDaily().trans_history()

    SecuritiesDaily().run()

    pass
