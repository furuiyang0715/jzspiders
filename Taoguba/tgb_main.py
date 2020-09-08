import os
import random
import sys

cur_path = os.path.split(os.path.realpath(__file__))[0]
file_path = os.path.abspath(os.path.join(cur_path, ".."))
sys.path.insert(0, file_path)

from Taoguba.taoguba import Taoguba
from base_spider import SpiderBase
from scripts import utils


class TgbSchedule(SpiderBase):
    table_name = 'taoguba'
    dt_benchmark = 'pub_date'

    def __init__(self):
        super(TgbSchedule, self).__init__()
        info = utils.org_tablecode_map.get(self.table_name)
        self.name, self.table_code = info[0], info[1]

    @property
    def keys(self):
        self._dc_init()
        sql = '''select SecuCode, ChiNameAbbr from const_secumain where SecuCode in (select distinct SecuCode from const_secumain); '''
        datas = self.dc_client.select_all(sql)
        keys = {r['SecuCode']: r['ChiNameAbbr'] for r in datas}
        return keys

    def convert_lower(self, order_book_id: str):
        """
        转换合约代码为前缀模式 并且前缀字母小写
        :param order_book_id:
        :return:
        """
        EXCHANGE_DICT = {
            "XSHG": "SH",
            "XSHE": "SZ",
            "INDX": "IX",
            "XSGE": "SF",
            "XDCE": "DF",
            "XZCE": "ZF",
            "CCFX": "CF",
            "XINE": "IF",
        }

        code, exchange = order_book_id.split('.')
        ex = EXCHANGE_DICT.get(exchange)
        return ''.join((ex, code)).lower()

    @property
    def lower_keys(self):
        lkeys = {}
        for key, value in self.keys.items():
            lkeys[self.convert_lower(key)] = value
        return lkeys

    def start(self):
        _keys = list(self.lower_keys.keys())
        random.shuffle(_keys)
        # print(_keys)
        for code in _keys:
            name = self.lower_keys.get(code)
            print(code, name)
            Taoguba(name, code).start()

    def trans_history(self):
        self._spider_init()
        for i in range(1000):    # TODO
            trans_sql = '''select pub_date as PubDatetime,\
code as SecuCode, \
chinameabbr as SecuAbbr, \
stockattr as Abstract,\
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
    # TgbSchedule().start()

    TgbSchedule().trans_history()

    pass
