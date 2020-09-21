# 自选股查询
import datetime
import json
import pprint
import sys
import time

import requests

from base_spider import SpiderBase


class JuChaoSearch(SpiderBase):
    def __init__(self):
        super(JuChaoSearch, self).__init__()
        self.table_name = 'juchao_ant'

    # def get_code_status(self):
    #     # api = '''http://uc.cninfo.com.cn/portfolio/getBatchStocksSelectedStatus'''
    #     text = '''{"list":[{"stockCode":"000895","organId":"gssz0000895","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":true},{"stockCode":"300117","organId":"9900013439","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"603288","organId":"9900023228","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"600519","organId":"gssh0600519","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"000651","organId":"gssz0000651","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":true},{"stockCode":"002726","organId":"9900023003","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"600887","organId":"gssh0600887","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"600566","organId":"gssh0600566","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"002372","organId":"9900011087","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false},{"stockCode":"601933","organId":"9900016367","stockName":null,"pinyin":null,"category":null,"sequence":null,"existInPortfolio":false}],"success":"true"}'''
    #     py_data = json.loads(text).get("list")
    #     _map = dict()
    #     for one in py_data:
    #         _map[one.get("stockCode")] = one.get("organId")
    #     return _map

    def create_tools_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS `juchao_codemap` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `code` varchar(8) NOT NULL COMMENT '证券代码',
            `orgId` varchar(16) NOT NULL COMMENT '证券编码',
            `category` varchar(8) NOT NULL COMMENT '证券分类',
            `pinyin` varchar(10) NOT NULL COMMENT '证券中文名拼音',
            `zwjc` varchar(20) NOT NULL COMMENT '证券中文名',
            `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
            `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            UNIQUE KEY `orgId_code` (`orgId`, `code`),
            KEY `update_time` (`UPDATETIMEJZ`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='巨潮证券编码';
        '''
        self._spider_init()
        self.spider_client.insert(sql)
        self.spider_client.end()

    def get_stock_json(self):
        # api = 'http://www.cninfo.com.cn/new/data/szse_a_stock.json?_=1600666894817'

        api = 'http://www.cninfo.com.cn/new/data/szse_a_stock.json?_={}'.format(int(time.time() * 1000))
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.cninfo.com.cn',
            'Origin': 'http://uc.cninfo.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://uc.cninfo.com.cn/user/optionalConfig?groupId=88937',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        }
        resp = requests.get(api, headers=headers)
        # print(resp)
        text = resp.text
        # print(text)
        py_data = json.loads(text).get("stockList")
        # print(py_data)
        # print(len(py_data))
        self._spider_init()
        fields = ['code', 'orgId', 'category', 'pinyin', 'zwjc']
        for one in py_data:
            self._save(self.spider_client, one, 'juchao_codemap', fields)

    def get_user_list(self):
        '''
        stock: 000651,gssz0000651;002841,9900029752
        searchkey:
        seDate: 2000-01-01~2020-09-21
        sortName: time
        sortType: desc
        tabName: qw
        pageNum: 1
        pageSize: 20
        '''

        url = '''http://www.cninfo.com.cn/new/userAnnouncement/getUserAnnouncementsList'''
        post_data = {
            # 'stock': '000651,gssz0000651;002841,9900029752',
            # 'stock': '002841,9900029752;601399,9900010450',
            'stock': '002841,9900029752;',
            'searchkey': '',
            'seDate': '2000-01-01~2020-09-21',
            'sortName': 'time',
            'sortType': 'desc',
            'tabName': 'qw',
            'pageNum': 1,
            'pageSize': 20,
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '149',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.cninfo.com.cn',
            'Origin': 'http://uc.cninfo.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://uc.cninfo.com.cn/user/optionalNotice',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',

        }

        resp = requests.post(url, data=post_data, headers=headers)
        text = resp.text
        py_data = json.loads(text)
        ants = py_data.get("announcements")
        for ant in ants:
            item = dict()
            item['id'] = ant.get("announcementId")
            item['SecuCode'] = ant.get("secCode")
            item['SecuAbbr'] = ant.get("secName")
            item['AntTitle'] = ant.get("announcementTitle")
            time_stamp = ant.get("announcementTime") / 1000
            ant_time = datetime.datetime.fromtimestamp(time_stamp)
            item['AntTime'] = ant_time
            item['AntDoc'] = "http://static.cninfo.com.cn/" + ant.get("adjunctUrl")
            print(item)
            '''
            {
            'adjunctSize': 320,
            'adjunctType': 'PDF',
            'adjunctUrl': 'finalpage/2020-09-17/1208450211.PDF',
            'announcementContent': '',
            'announcementId': '1208450211',
            'announcementTime': 1600272000000,
            'announcementTitle': '关于2018年限制性股票激励计划首次授予限制性股票第二个解除限售期解除限售股份上市流通的提示性公告',
            'announcementType': '01010503||010112||010114||01130340||012325',
            'announcementTypeName': None,
            'associateAnnouncement': None,
            'batchNum': None,
            'columnId': '01010301||01010302||01010411||09020202||250201||251302||2705',
            'id': None,
            'important': None,
            'orgId': '9900029752',
            'orgName': None,
            'pageColumn': 'SZZX',
            'secCode': '002841',
            'secName': '视源股份',
            'storageTime': None, 
            }
            
            '''

    def create_spider_table(self):
        sql = '''
         CREATE TABLE IF NOT EXISTS `{}` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `SecuCode` varchar(8) NOT NULL COMMENT '证券代码',
          `SecuAbbr` varchar(16) NOT NULL COMMENT '证券代码',
          `AntTime` datetime NOT NULL COMMENT '发布时间',
          `AntTitle` varchar(128) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯标题',
          `AntDoc` varchar(256) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '公告详情页链接',
          `category` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '资讯类别',
          `CREATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP,
          `UPDATETIMEJZ` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `code_doc` (`SecuCode`,`AntDoc`),
          KEY `ant_time` (`AntTime`),
          KEY `update_time` (`UPDATETIMEJZ`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='巨潮个股公告关联';  
        '''.format(self.table_name)

        pass

    def get_ant_type(self):
        _map = dict()
        category = [
            {"key": "category_ndbg_szsh", "value": "年报"},
            {"key": "category_bndbg_szsh", "value": "半年报"},
            {"key": "category_yjdbg_szsh", "value": "一季报"},
            {"key": "category_sjdbg_szsh", "value": "三季报"},
            {"key": "category_yjygjxz_szsh", "value": "业绩预告"},
            {"key": "category_qyfpxzcs_szsh", "value": "权益分派"},
            {"key": "category_dshgg_szsh", "value": "董事会"},
            {"key": "category_jshgg_szsh", "value": "监事会"},
            {"key": "category_gddh_szsh", "value": "股东大会"},
            {"key": "category_rcjy_szsh", "value": "日常经营"},
            {"key": "category_gszl_szsh", "value": "公司治理"},
            {"key": "category_zj_szsh", "value": "中介报告"},
            {"key": "category_sf_szsh", "value": "首发"},
            {"key": "category_zf_szsh", "value": "增发"},
            {"key": "category_gqjl_szsh", "value": "股权激励"},
            {"key": "category_pg_szsh", "value": "配股"},
            {"key": "category_jj_szsh", "value": "解禁"},
            {"key": "category_gszq_szsh", "value": "公司债"},
            {"key": "category_kzzq_szsh", "value": "可转债"},
            {"key": "category_qtrz_szsh", "value": "其他融资"},
            {"key": "category_gqbd_szsh", "value": "股权变动"},
            {"key": "category_bcgz_szsh", "value": "补充更正"},
            {"key": "category_cqdq_szsh", "value": "澄清致歉"},
            {"key": "category_fxts_szsh", "value": "风险提示"},
            {"key": "category_tbclts_szsh", "value": "特别处理和退市"},
            {"key": "category_tszlq_szsh", "value": "退市整理期"}
        ]
        for one in category:
            _map[one.get("key")] = one.get("value")

        print(pprint.pformat(_map))
        return _map


if __name__ == '__main__':
    ins = JuChaoSearch()
    # ins.create_tools_table()
    # ins.get_stock_json()

    # ins.get_user_list()

    ins.get_ant_type()
