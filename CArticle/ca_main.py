import os
import random
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from CArticle.ca_spider import CArticleSpiser
from base_spider import SpiderBase
from scripts import utils


class CaSchedule(SpiderBase):
    table_name = "eastmoney_carticle"

    def __init__(self):
        super(CaSchedule, self).__init__()
        self.keys = list(self.dc_info().values())
        random.shuffle(self.keys)
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def dc_info(self):
        self._dc_init()
        sql = '''select SecuCode, ChiNameAbbr from const_secumain where SecuCode \
            in (select distinct SecuCode from const_secumain);'''
        datas = self.dc_client.select_all(sql)
        dc_info = {r['SecuCode']: r['ChiNameAbbr'] for r in datas}
        return dc_info

    def run(self, key):
        CArticleSpiser(key=key).start()

    def _create_table(self):
        self._spider_init()
        sql = '''
           CREATE TABLE IF NOT EXISTS `{}` (
             `id` int(11) NOT NULL AUTO_INCREMENT,
             `pub_date` datetime NOT NULL COMMENT '发布时间',
             `code` varchar(16) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '股票代码',
             `title` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章标题',
             `link` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章详情页链接',
             `article` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '详情页内容',
             `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
             `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
             PRIMARY KEY (`id`),
             UNIQUE KEY `link` (`link`),
             KEY `pub_date` (`pub_date`),
             KEY `update_time` (`UPDATETIMEJZ`)
           ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='东财-财富号文章'; 
           '''.format(self.table_name)
        self.spider_client.insert(sql)
        self.spider_client.end()

    def start(self):
        self._create_table()
        for key in self.keys:
            print("当前的主题是: {}".format(key))
            self.run(key)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
code as SecuCode, \
title as Title,\
link as Website,\
article as Content, \
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


if __name__ == "__main__":
    # CaSchedule().start()

    CaSchedule().trans_history()

    pass
