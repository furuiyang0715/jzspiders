import os
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from ShangHaiSecuritiesNews.cn_4_hours import CN4Hours
from ShangHaiSecuritiesNews.cn_hongguan import CNStock
from base_spider import SpiderBase
from scripts import utils


class CNSchedule(SpiderBase):
    """上海证券报 爬虫调度"""
    class_lst = [
        CN4Hours,  # 上证 4 小时
        CNStock,  # 宏观等 ...
    ]

    table_name = 'cn_stock'
    # name = '上海证券报'
    info = utils.org_tablecode_map.get(table_name)
    name, table_code = info[0], info[1]

    def __init__(self):
        super(CNSchedule, self).__init__()

    def ins_start(self, instance):
        instance.start()

    def start(self):
        for cls in self.class_lst:
            ins = cls()
            print(ins.name)
            ins.start()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def run(self):
        for cls in self.class_lst:
            ins = cls()
            print(ins.name)
            ins.run()

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
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
    # CNSchedule().start()

    # CNSchedule().trans_history()

    CNSchedule().run()

    pass
