import datetime
import json
import os
import sys
import time

import requests

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from base_spider import SpiderBase
from scripts import utils


class XueQiuKuaiXun(SpiderBase):
    def __init__(self):
        super(XueQiuKuaiXun, self).__init__()
        self.web_url = 'https://xueqiu.com/today#/livenews'
        self.first_api = 'https://xueqiu.com/statuses/livenews/list.json?since_id=-1&max_id=-1&count=10'
        self.base_api = 'https://xueqiu.com/statuses/livenews/list.json?since_id=-1&max_id={}&count=15'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
            # 'Cookie': 's=dk1af2e0xx; device_id=225b7001f44831dd2c0ef9a0a27c309c; __utma=1.390898764.1595042617.1595042617.1595042617.1; __utmz=1.1595042617.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAADZ1qkEJjAIA4U5tcaMBWxG5jhDi; xq_a_token=4db837b914fc72624d814986f5b37e2a3d9e9944; xqat=4db837b914fc72624d814986f5b37e2a3d9e9944; xq_r_token=2d6d6cc8e57501dfe571d2881cabc6a5f2542bf8; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYwMDQ4MzAwNywiY3RtIjoxNTk3OTE1NjU0NjMzLCJjaWQiOiJkOWQwbjRBWnVwIn0.Xv18aNMnTCbBSBdBeEBlebGCJRVna9F89ghYs2iTc2zXztEJJ6az2lWMX7E78Nt1aVY97kPhNMs0IcCtHWX7WOX3xqZMUQpUi_ZbDTv7vUoOIBKB27jtenSkM6i_u3pgDrVvyXngbcnof-zKv86LzfcgQSCL3GcnmtwHFmoXctumpD8Z400r3m753u7uNnFOptyGJaIDIqvcF6vlBjm01b18WwYrkjIcW3ujJPGkTr38O9FYujILUQjCdRQZsTgEQfK3bPWeOJNFd8V9rMXl0tZlYN7m1yhL1DYeMqyTvCY5rvkzUQ6cWyBJJZ615auqmflzwe__i-reu-6D_6U53w; u=561597915688189; Hm_lvt_1db88642e346389874251b5a1eded6e3=1597915690,1597990683; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1597990683',
            'Cookie': 's=dk1af2e0xx; device_id=225b7001f44831dd2c0ef9a0a27c309c; __utma=1.390898764.1595042617.1595042617.1595042617.1; __utmz=1.1595042617.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAADZ1qkEJjAIA4U5tcaMBWxG5jhDi; Hm_lvt_1db88642e346389874251b5a1eded6e3=1597915690,1597990683,1597991491,1597991681; acw_tc=2760821816003959123427825e841d81c725fc4dd911b56880e7c2c47408c5; xq_a_token=636e3a77b735ce64db9da253b75cbf49b2518316; xqat=636e3a77b735ce64db9da253b75cbf49b2518316; xq_r_token=91c25a6a9038fa2532dd45b2dd9b573a35e28cfd; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYwMjY0MzAyMCwiY3RtIjoxNjAwMzk1ODk5MDA3LCJjaWQiOiJkOWQwbjRBWnVwIn0.T9p8r7uzAePqX9W6BstadlZ2inHVwkfTXcL6-CsWhp9Cg_uQc9WGoWCTUcMVSP10nGyEvR7hlgK5b6_atsTB8Ke9eXDy4nNLwlflY8u4XVN-8lBgxSko2DMGV2H3pQdQmswCwxb9ZS31elEd8o13Q2ATR9OF1U5KnJZUx8fRrIBrtBlWYBytF_0PNHrfpX7Ka0lp8IunKD7UAsECZTcKLho6wXrQwdsL4__OElA2KDvoU2-oq8mq7sf7IpnlNALJPIqq6-TJip0UunIoryAIGv2vzKu8i3G8OLlJU9argup9dliQgemYPHFi3cFXF_FRzzskVi7rzFfD7yNmOYfEAw; u=121600395921114; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1600395922',

        }
        self.table_name = 'xueqiu_livenews'
        # self.name = '雪球快讯'
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]
        self.fields = ['link', 'pub_date', 'text']

    def _create_table(self):
        self._spider_init()
        sql = '''
        CREATE TABLE IF NOT EXISTS `{}`(
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `pub_date` datetime NOT NULL COMMENT '发布时间',
          `link` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯详情页链接',
          `text` text CHARACTER SET utf8 COLLATE utf8_bin COMMENT '详情页内容',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          KEY `pub_date` (`pub_date`), 
          UNIQUE KEY `date_id` (`pub_date`, `id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{}';
        '''.format(self.table_name, self.name)
        self.spider_client.insert(sql)
        self.spider_client.end()

    def fetch_datas(self, url):
        resp = requests.get(url, headers=self.headers)
        if resp and resp.status_code == 200:
            text = resp.text
            datas = json.loads(text)
            next_max_id = datas.get("next_max_id")
            next_url = self.base_api.format(next_max_id)
            items = datas.get("items")
            to_insert_lst = []
            for item in items:
                _pub_date = datetime.datetime.fromtimestamp(int(item.get("created_at") / 1000))
                to_insert = {
                    "pub_date": _pub_date,
                    "text": item.get("text"),
                    "link": item.get("link"),
                    'id': item.get("id"),
                }
                print(to_insert)
                to_insert_lst.append(to_insert)
                # if _pub_date < datetime.datetime.combine(datetime.datetime.today(), datetime.time.min):
                if _pub_date < datetime.datetime.now() - datetime.timedelta(minutes=60):
                    self._batch_save(self.spider_client, to_insert_lst, self.table_name, self.fields)
                    return None
            self._batch_save(self.spider_client, to_insert_lst, self.table_name, self.fields)
            return next_url

    def start(self):
        self._create_table()
        next_url = self.fetch_datas(self.first_api)
        while next_url:
            print(next_url)
            next_url = self.fetch_datas(next_url)
            time.sleep(1)

    #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _fetch_datas(self, url):
        resp = requests.get(url, headers=self.headers)
        print(resp)
        if resp and resp.status_code == 200:
            text = resp.text
            datas = json.loads(text)
            next_max_id = datas.get("next_max_id")
            next_url = self.base_api.format(next_max_id)
            items = datas.get("items")
            for item in items:
                _pub_date = datetime.datetime.fromtimestamp(int(item.get("created_at") / 1000))

                to_insert = {
                    "PubDatetime": _pub_date,
                    "Content": item.get("text"),
                    "Website": item.get("link"),
                    'Title': item.get("text")[:20],
                    'DupField': "{}_{}".format(self.table_code, item.get("id")),
                    'MedName': self.name,
                    'OrgMedName': self.name,
                    'OrgTableCode': self.table_code,
                }

                self._save(self.spider_client, to_insert, self.merge_table, self.merge_fields)
                if _pub_date < datetime.datetime.now() - datetime.timedelta(minutes=60):
                    return None
            return next_url

    def run(self):
        self._spider_init()
        next_url = self._fetch_datas(self.first_api)
        print(next_url)
        while next_url:
            print(next_url)
            next_url = self._fetch_datas(next_url)
            time.sleep(1)

    def trans_history(self):
        self._spider_init()
        for i in range(1000):  # TODO
            trans_sql = '''select pub_date as PubDatetime,\
link as Website,\
text as Content, \
CREATETIMEJZ as CreateTime, \
UPDATETIMEJZ as UpdateTime, id \
from {} limit {}, 1000; '''.format(self.table_name, i * 1000)
            datas = self.spider_client.select_all(trans_sql)
            print(len(datas))
            if not datas:
                break
            for data in datas:
                data['Title'] = data['Content'][:20]
                data['DupField'] = "{}_{}".format(self.table_code, data['id'])
                data['MedName'] = self.name
                data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


if __name__ == '__main__':
    # XueQiuKuaiXun().start()

    # XueQiuKuaiXun().trans_history()

    XueQiuKuaiXun().run()

    pass
