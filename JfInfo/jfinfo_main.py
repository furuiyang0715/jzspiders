import os
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from JfInfo.reference import HKInfo, Reference, Research, TZZJY
from base_spider import SpiderBase
from scripts import utils


class JFSchedule(SpiderBase):
    """巨丰财经 爬虫调度"""
    class_lst = [
        HKInfo,  # 港股资讯
        Reference,  # 巨丰内参
        Research,  # 巨丰研究院
        TZZJY,  # 投资者教育
    ]

    table_name = 'jfinfo'
    # dt_benchmark = 'pub_date'
    # name = '巨丰财经'

    info = utils.org_tablecode_map.get(table_name)
    name, table_code = info[0], info[1]

    def ins_start(self, instance):
        instance.start()

    def start(self):
        for cls in self.class_lst:
            ins = cls()
            print(f"巨丰财经 --> {ins.name}")
            ins.start()

    def trans_history(self):
        self._spider_init()
        for i in range(1000):  # TODO
            trans_sql = '''select pub_date as PubDatetime,\
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
                data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


if __name__ == "__main__":
    # JFSchedule().start()

    JFSchedule().trans_history()
