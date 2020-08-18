import os
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from ShangHaiSecuritiesNews.cn_4_hours import CN4Hours
from ShangHaiSecuritiesNews.cn_hongguan import CNStock


class CNSchedule(object):
    """上海证券报 爬虫调度"""
    class_lst = [
        CN4Hours,  # 上证 4 小时
        CNStock,  # 宏观等 ...
    ]

    table_name = 'cn_stock'
    # dt_benchmark = 'pub_date'
    name = '上海证券报'

    def ins_start(self, instance):
        instance.start()

    def start(self):
        for cls in self.class_lst:
            ins = cls()
            print(ins.name)
            ins.start()


if __name__ == "__main__":
    cns = CNSchedule()
    cns.start()
