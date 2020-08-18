import os
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from JfInfo.reference import HKInfo, Reference, Research, TZZJY


class JFSchedule(object):
    """巨丰财经 爬虫调度"""
    class_lst = [
        HKInfo,  # 港股资讯
        Reference,  # 巨丰内参
        Research,  # 巨丰研究院
        TZZJY,  # 投资者教育
    ]

    table_name = 'jfinfo'
    # dt_benchmark = 'pub_date'
    name = '巨丰财经'

    def ins_start(self, instance):
        instance.start()

    def start(self):
        for cls in self.class_lst:
            ins = cls()
            print(f"巨丰财经 --> {ins.name}")
            ins.start()


if __name__ == "__main__":
    JFSchedule().start()
