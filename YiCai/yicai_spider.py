import datetime
import json
import os
import sys

import requests
from lxml import html

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from base_spider import SpiderBase
from scripts import utils


class YiCai(SpiderBase):
    def __init__(self):
        super(YiCai, self).__init__()
        self.index_url = 'https://www.yicai.com/'
        self.url = 'https://www.yicai.com/api/ajax/getlatest?page={}&pagesize=25'
        self.table_name = 'NewsYicai'
        # self.name = '第一财经新闻'
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]
        self.fields = ['pub_date', 'author', 'source', 'title', 'link', 'article']

    def fetch_detail_page(self, url):
        article = None
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            body = resp.text
            doc = html.fromstring(body)
            try:
                article = doc.xpath(".//div[@class='m-txt']")[0].text_content()
            except:
                pass
        return article

    def get_list_items(self, page):
        items = []
        resp = requests.get(self.url.format(page))
        if resp and resp.status_code == 200:
            body = resp.text
            datas = json.loads(body)
            for one in datas:
                # print(pprint.pformat(one))
                item = dict()
                _date_str = one.get("LastDate")
                _date = datetime.datetime.strptime(_date_str, "%Y-%m-%dT%H:%M:%S")
                item['pub_date'] = _date
                _url = one.get("url")
                if "video" in _url:
                    continue
                link = "https://www.yicai.com" + _url
                item['link'] = link
                item['title'] = one.get("NewsTitle")
                item['source'] = one.get("NewsSource")
                item['author'] = one.get("NewsAuthor")
                detail = self.fetch_detail_page(link)
                item['article'] = detail
                items.append(item)
        return items

    def _create_table(self):
        self._spider_init()
        sql = '''
       CREATE TABLE IF NOT EXISTS `{}` (
         `id` int(11) NOT NULL AUTO_INCREMENT,
         `pub_date` datetime NOT NULL COMMENT '发布时间',
         `author` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '新闻作者',
         `source` varchar(32) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '新闻来源',
         `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin COMMENT '文章标题',
         `link` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin COMMENT '文章详情页链接',
         `article` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '详情页内容',
         `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
         `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
         PRIMARY KEY (`id`),
         UNIQUE KEY `link` (`link`),
         KEY `pub_date` (`pub_date`),
         KEY `update_time` (`UPDATETIMEJZ`)
       ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{}'; 
       '''.format(self.table_name, self.name)
        self.spider_client.insert(sql)
        self.spider_client.end()

    def start(self):
        self._create_table()
        self._spider_init()
        for page in range(1, 2):
            items = self.get_list_items(page)
            print(f'{self.name} 本页爬取个数{len(items)}')
            ret = self._batch_save(self.spider_client, items, self.table_name, self.fields)
            print(f'{self.name} 本页入库个数{ret}')

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _get_list_items(self, page):
        resp = requests.get(self.url.format(page))
        if resp and resp.status_code == 200:
            body = resp.text
            datas = json.loads(body)
            for one in datas:
                item = dict()
                _date_str = one.get("LastDate")
                _date = datetime.datetime.strptime(_date_str, "%Y-%m-%dT%H:%M:%S")
                item['PubDatetime'] = _date
                _url = one.get("url")
                if "video" in _url:
                    continue
                link = "https://www.yicai.com" + _url
                item['Website'] = link
                item['Title'] = one.get("NewsTitle")
                item['OrgMedName'] = one.get("NewsSource")
                # item['author'] = one.get("NewsAuthor")
                detail = self.fetch_detail_page(link)
                item['Content'] = detail
                # 增加合并字段
                item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                item['MedName'] = self.name
                if not item['OrgMedName']:
                    item['OrgMedName'] = self.name
                item['OrgTableCode'] = self.table_code
                self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def run(self):
        self._spider_init()
        for page in range(1, 2):
            self._get_list_items(page)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):  # TODO
            trans_sql = '''select pub_date as PubDatetime,\
source as OrgMedName, \
title as Title,\
link as Website,\
article as Content, \
CREATETIMEJZ as CreateTime, \
UPDATETIMEJZ as UpdateTime \
from {} limit {}, 1000; '''.format(self.table_name, i * 1000)
            datas = self.spider_client.select_all(trans_sql)
            print(len(datas))
            if not datas:
                break
            for data in datas:
                data['DupField'] = "{}_{}".format(self.table_code, data['Website'])
                data['MedName'] = self.name
                if not data['OrgMedName']:
                    data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


if __name__ == "__main__":
    # YiCai().start()

    # YiCai().trans_history()

    YiCai().run()

    pass
