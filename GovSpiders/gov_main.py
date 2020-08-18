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


class ChinaBankSchedule(object):
    class_lst = [
        ChinaBankShuJuJieDu,
        ChinaBankXinWenFaBu
    ]

    table_name = 'chinabank'
    name = '中国银行'

    def ins_start(self, instance):
        instance.start()

    def start(self):
        """顺次运行"""
        for cls in self.class_lst:
            ins = cls()
            print(f"中国银行 --> {ins.name}")
            ins.start()


class GovStatsSchedule(object):
    class_lst = [
        GovStatsShuJuJieDu,
        GovStatsTongJiDongTai,
        GovStatsXinWenFaBuHui,
        GovStatsZuiXinFaBu,
    ]

    table_name = 'gov_stats'
    name = '国家统计局'

    def start(self):
        """顺次运行"""
        for cls in self.class_lst:
            ins = cls()
            print(f"中国银行 --> {ins.name}")
            ins.start()


if __name__ == "__main__":
    ChinaBankSchedule().start()
    GovStatsSchedule().start()
