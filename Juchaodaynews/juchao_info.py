import json
import math
import os
import sys
import time
import requests

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from base_spider import SpiderBase
from scripts import utils


class JuChaoInfo(SpiderBase):
    def __init__(self):
        super(JuChaoInfo, self).__init__()
        self.web_url = 'http://webapi.cninfo.com.cn/#/aiInfos'
        self.zuixin_url = "http://webapi.cninfo.com.cn//api/sysapi/p_sysapi1128"
        self.stock_url = "http://webapi.cninfo.com.cn//api/sysapi/p_sysapi1078"
        self.fund_url = "http://webapi.cninfo.com.cn//api/sysapi/p_sysapi1126"
        self.datas_url = "http://webapi.cninfo.com.cn//api/sysapi/p_sysapi1127"
        self.mcode = self._generate_mcode()
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Cookie': '__qc_wId=726; pgv_pvid=6020356972; Hm_lvt_489bd07e99fbfc5f12cbb4145adb0a9b=1581945588; codeKey=ce7a9a719b; Hm_lpvt_489bd07e99fbfc5f12cbb4145adb0a9b=1582016401',
            'Host': 'webapi.cninfo.com.cn',
            'mcode': '{}'.format(self.mcode),
            'Origin': 'http://webapi.cninfo.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://webapi.cninfo.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.fields = ['code', 'pub_date', 'title', 'category', 'summary']
        self.table_name = "juchao_info"
        # self.name = '巨潮AI资讯'
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def _generate_mcode(self):
        dt = str(math.floor(time.time()))
        keyStr = "ABCDEFGHIJKLMNOP" + "QRSTUVWXYZabcdef" + "ghijklmnopqrstuv" + "wxyz0123456789+/" + "="
        output = ""
        i = 0
        while i < len(dt):
            try:
                chr1 = ord(dt[i])
            except IndexError:
                chr1 = 0
            i += 1

            try:
                chr2 = ord(dt[i])
            except IndexError:
                chr2 = 0
            i += 1

            try:
                chr3 = ord(dt[i])
            except:
                chr3 = 0
            i += 1

            enc1 = chr1 >> 2
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
            enc4 = chr3 & 63
            if not chr2:
                enc3 = enc4 = 64
            elif not chr3:
                enc4 = 64
            output = output + keyStr[enc1] + keyStr[enc2] + keyStr[enc3] + keyStr[enc4]
        return output

    def _get(self, url):
        resp = requests.post(url, headers=self.headers)
        if resp.status_code == 200:
            return resp.text

    def get_list(self, url):
        body = self._get(url)
        py_data = json.loads(body)
        result_code = py_data.get("resultcode")
        if result_code == 200:
            records = py_data.get("records")
            return records

    def _create_table(self):
        self._spider_init()
        sql = '''
         CREATE TABLE IF NOT EXISTS `{}` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `code` varchar(8) NOT NULL COMMENT '证券代码',
          `pub_date` datetime NOT NULL COMMENT '发布时间',
          `title` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯标题',
          `category` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯类别',
          `summary` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '资讯摘要',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `code_title` (`code`,`title`),
          KEY `pub_date` (`pub_date`),
          KEY `update_time` (`UPDATETIMEJZ`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='巨潮AI资讯'; 
        '''.format(self.table_name)
        self.spider_client.insert(sql)
        self.spider_client.end()

    def process_records(self, records, type_code):
        items = []
        for record in records:
            item = dict()
            pub_date = record.get("DECLAREDATE")
            if not pub_date:
                pub_date = record.get("RECTIME")
            item['pub_date'] = pub_date  # 发布时间
            item['code'] = record.get("SECCODE")  # 证券代码
            item['title'] = record.get("F001V")  # 资讯标题
            item['category'] = record.get("F003V")   # 资讯类别
            item['summary'] = record.get("F002V")   # 资讯摘要

            # item['pdf_link'] = record.get("F004V")    # pdf 链接
            # code = record.get("SECCODE")    # 文章编号
            # link = "http://webapi.cninfo.com.cn/#/aidetail?type=sysapi/p_sysapi{}&scode={}".format(type_code, code)
            # item['link'] = link
            # print(item)
            items.append(item)
        return items

    def start(self):
        self._create_table()
        self._spider_init()

        zuixin_records = self.get_list(self.zuixin_url)
        zuixin_items = self.process_records(zuixin_records, 1128)

        stock_records = self.get_list(self.stock_url)
        stock_items = self.process_records(stock_records, 1078)

        fund_records = self.get_list(self.fund_url)
        fund_items = self.process_records(fund_records, 1126)

        datas_records = self.get_list(self.datas_url)
        datas_items = self.process_records(datas_records, 1127)

        for items in (zuixin_items, stock_items, fund_items, datas_items):
            save_num = self._batch_save(self.spider_client, items, self.table_name, self.fields)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _process_records(self, records, type_code):
        for record in records:
            item = dict()
            pub_date = record.get("DECLAREDATE")
            if not pub_date:
                pub_date = record.get("RECTIME")
            item['PubDatetime'] = pub_date  # 发布时间
            item['SecuCode'] = record.get("SECCODE")  # 证券代码
            item['Title'] = record.get("F001V")  # 资讯标题
            item['InnerType'] = record.get("F003V")   # 资讯类别
            item['Content'] = record.get("F002V")   # 资讯摘要
            # 增加合并表字段
            item['DupField'] = "{}_{}_{}".format(self.table_code, item['SecuCode'], item['Title'])
            item['MedName'] = self.name
            item['OrgMedName'] = self.name
            item['OrgTableCode'] = self.table_code
            self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def run(self):
        self._spider_init()

        zuixin_records = self.get_list(self.zuixin_url)
        self._process_records(zuixin_records, 1128)

        stock_records = self.get_list(self.stock_url)
        self._process_records(stock_records, 1078)

        fund_records = self.get_list(self.fund_url)
        self._process_records(fund_records, 1126)

        datas_records = self.get_list(self.datas_url)
        self._process_records(datas_records, 1127)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
code as SecuCode, \
title as Title,\
category as InnerType,\
summary as Content, \
CREATETIMEJZ as CreateTime, \
UPDATETIMEJZ as UpdateTime \
from {} limit {}, 1000; '''.format(self.table_name, i*1000)
            datas = self.spider_client.select_all(trans_sql)
            print(len(datas))
            if not datas:
                break
            for data in datas:
                data['DupField'] = "{}_{}_{}".format(self.table_code, data['SecuCode'], data['Title'])
                data['MedName'] = self.name
                data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


if __name__ == "__main__":
    # JuChaoInfo().start()

    # JuChaoInfo().trans_history()

    JuChaoInfo().run()

    pass
