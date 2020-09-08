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


if __name__ == "__main__":
    ChinaBankSchedule().start()

    GovStatsSchedule().start()

    pass
