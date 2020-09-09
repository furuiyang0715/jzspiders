import os
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)


from Takungpao.economic_observer import EconomicObserver
from Takungpao.hkstock_cjss import HKStock_CJSS, HKStock_GJJJ, HKStock_GSYW, HKStock_JGSD, HKStock_JJYZ, HKStock_QQGS
from Takungpao.takungpao_fk import FK
from Takungpao.takungpao_travel import Travel
from Takungpao.zhongguojingji import Business, DiChan, GuoJiJingJi, HKStock, HKCaiJing, NewFinanceTrend, ZhongGuoJingJi
from base_spider import SpiderBase
from scripts import utils


class TakungpaoSchedule(SpiderBase):
    """大公报 爬虫调度"""
    class_lst = [
        Business,  # 商业
        DiChan,  # 地产
        EconomicObserver,  # 经济观察家
        GuoJiJingJi,  # 国际经济
        HKStock,  # 港股
        HKCaiJing,  # 香港财经
        HKStock_CJSS,  # 财经时事
        HKStock_GJJJ,  # 国际聚焦
        HKStock_GSYW,  # 公司要闻
        HKStock_JGSD,  # 机构视点
        HKStock_JJYZ,  # 经济一周
        HKStock_QQGS,  # 全球股市
        NewFinanceTrend,  # 新经济浪潮
        FK,  # 风口
        Travel,  # 旅游
        ZhongGuoJingJi,  # 中国经济
    ]

    table_name = 'Takungpao'

    def __init__(self):
        super(TakungpaoSchedule, self).__init__()
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    def ins_start(self, instance):
        instance.start()

    def start(self):
        """顺次运行"""
        for cls in self.class_lst:
            ins = cls()
            print(f"大公报 --> {ins.name}")
            ins.start()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def run(self):
        for cls in self.class_lst:
            ins = cls()
            print(f"大公报 --> {ins.type}")
            ins.run()

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
title as Title,\
link as Website,\
article as Content, \
source as OrgMedName, \
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
                if not data['OrgMedName']:
                    data['OrgMedName'] = self.name
                data['OrgTableCode'] = self.table_code
                self._save(self.spider_client, data, 'OriginSpiderAll', self.merge_fields)


if __name__ == "__main__":
    # TakungpaoSchedule().start()

    # TakungpaoSchedule().trans_history()

    TakungpaoSchedule().run()

    pass
