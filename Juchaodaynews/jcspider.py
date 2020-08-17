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


class JuchaoDayNews(SpiderBase):
    def __init__(self):
        super(JuchaoDayNews, self).__init__()
        # self.web_url = 'http://www.cninfo.com.cn/new/commonUrl/quickNews?url=/disclosure/quickNews&queryDate=2020-08-13'
        self.api_url = 'http://www.cninfo.com.cn/new/quickNews/queryQuickNews?queryDate={}&type='
        self.headers = {
            # 'Host': 'www.cninfo.com.cn',
            # 'Referer': 'http://www.cninfo.com.cn/new/commonUrl/quickNews?url=/disclosure/quickNews&queryDate=2020-08-14',
            # 'Cookie': 'JSESSIONID=1D4A040A6D5326C992FAD7DD8FFD946A; _sp_ses.2141=*; UC-JSESSIONID=DD0F58092C1828107B9921E3436A935B; _sp_id.2141=a878da76-08ce-42a8-9c5b-7e4ec1df3721.1597628172.1.1597630509.1597628172.58921c96-de2a-4c69-b2be-b1b2a79635c3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        }
        self.fields = ['code', 'name', 'link', 'title', 'type', 'pub_date']
        self.table_name = 'juchao_kuaixun'
        self.name = '巨潮快讯'
        self._juyuan_init()
        self._spider_init()

    def get_secu_abbr(self, code):
        sql = '''select SecuAbbr from secumain where secucode = '{}';'''.format(code)
        name = self.juyuan_client.select_one(sql).get("SecuAbbr")
        return name

    def _create_table(self):
        sql = '''
         CREATE TABLE IF NOT EXISTS `{}` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `code` varchar(8) DEFAULT NULL COMMENT '证券代码',
          `name` varchar(16) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '证券简称', 
          `pub_date` datetime NOT NULL COMMENT '发布时间',
          `title` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯标题',
          `type` varchar(16) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯类别',
          `link` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '公告详情页链接',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `date_title` (`pub_date`, `title`),
          KEY `pub_date` (`pub_date`),
          KEY `update_time` (`UPDATETIMEJZ`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{}'; 
        '''.format(self.table_name, self.name)
        self.spider_client.insert(sql)
        self.spider_client.end()

    def start(self):
        self._create_table()
        start_day = datetime.datetime(2020, 6, 1)
        # start_day = datetime.datetime(2020, 8, 13)
        end_day = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
        # print(start_day)
        # print(end_day)
        _day = start_day
        while _day <= end_day:
            _day_str = _day.strftime("%Y-%m-%d")
            # print(_day_str)
            resp = requests.get(self.api_url.format(_day_str), headers=self.headers)
            if resp and resp.status_code == 200:
                text = resp.text
                # print(text)
                datas = json.loads(text)
                if not datas:
                    print("{} 无公告数据".format(_day_str))
                else:
                    # 保存数据
                    items = []
                    for data in datas:
                        print(data)
                        item = {}
                        # 需要保存的字段: 快讯的发布详细时间、类型、标题、地址、股票代码、股票名称
                        announcementTime = time.localtime(int(data.get("announcementTime") / 1000))
                        announcementTime = time.strftime("%Y-%m-%d %H:%M:%S", announcementTime)
                        item['pub_date'] = announcementTime

                        item['type'] = data.get("type")
                        item['title'] = data.get("title")
                        item['link'] = data.get("pagePath")
                        code = data.get("code")
                        if code:
                            item['code'] = code
                            item['name'] = self.get_secu_abbr(code)
                        print(item)
                        items.append(item)
                        print()
                    self._batch_save(self.spider_client, items, self.table_name, self.fields)
            _day += datetime.timedelta(days=1)
            time.sleep(2)


if __name__ == '__main__':
    jc = JuchaoDayNews()
    jc.start()

    # jc.get_secu_abbr("601827")
