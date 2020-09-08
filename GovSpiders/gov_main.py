import os
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from GovSpiders.china_bank import ChinaBankShuJuJieDu, ChinaBankXinWenFaBu
from GovSpiders.gov_stats_sjjd import GovStatsShuJuJieDu
from GovSpiders.gov_stats_tjdt import GovStatsTongJiDongTai
from GovSpiders.gov_stats_xwfbh import GovStatsXinWenFaBuHui
from GovSpiders.gov_stats_zxfb import GovStatsZuiXinFaBu
from scripts import utils
from base_spider import SpiderBase


class ChinaBankSchedule(SpiderBase):
    class_lst = [
        ChinaBankShuJuJieDu,
        ChinaBankXinWenFaBu
    ]

    table_name = 'chinabank'
    # name = '中国银行'

    def __init__(self):
        super(ChinaBankSchedule, self).__init__()
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def ins_start(self, instance):
        instance.start()

    def start(self):
        """顺次运行"""
        for cls in self.class_lst:
            ins = cls()
            print(f"中国银行 --> {ins.name}")
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


class GovStatsSchedule(SpiderBase):
    class_lst = [
        GovStatsShuJuJieDu,
        GovStatsTongJiDongTai,
        GovStatsXinWenFaBuHui,
        GovStatsZuiXinFaBu,
    ]

    table_name = 'gov_stats'
    # name = '国家统计局'

    def __init__(self):
        super(GovStatsSchedule, self).__init__()
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def start(self):
        """顺次运行"""
        for cls in self.class_lst:
            ins = cls()
            print(f"中国银行 --> {ins.name}")
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
    # ChinaBankSchedule().start()
    ChinaBankSchedule().trans_history()

    # GovStatsSchedule().start()
    GovStatsSchedule().trans_history()

    pass
