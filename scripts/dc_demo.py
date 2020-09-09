from base_spider import SpiderBase


class DCDemo(SpiderBase):
    def __init__(self):
        super(DCDemo, self).__init__()
        self._spider_init()

    def add_field_to_eastmoney_articles(self):
        '''
        ALTER TABLE eastmoney_carticle ADD IsMeg TINYINT(4) DEFAULT 0 COMMENT '是否进入汇总表';
        '''

        pass

    def start(self):

        '''
        select DupField from OriginSpiderAll where OrgTableCode = 1004;
        select link from eastmoney_carticle where IsMeg = 0 limit 10;


        select substring_index(DupField, "_", -1) from OriginSpiderAll;


        update eastmoney_carticle set IsMeg = 1 where link in (select B.link from OriginSpiderAll as A inner join eastmoney_carticle as B on substring_index(A.DupField, "_", -1) = B.link);
        update eastmoney_carticle set IsMeg = 1 where link in (select link from OriginSpiderAll inner join eastmoney_carticle on substring_index(OriginSpiderAll.DupField, "_", -1) = eastmoney_carticle.link);
        # ERROR 1093 (HY000): You can't specify target table 'eastmoney_carticle' for update in FROM clause

        update eastmoney_carticle set IsMeg = 1 where link in (select B.link from (select B.link from OriginSpiderAll as A inner join eastmoney_carticle as B on substring_index(A.DupField, "_", -1) = B.link ) B);
        # ok

        '''
        sql1 = '''select link from eastmoney_carticle where IsMeg = 0 limit 10 ;'''
        datas = self.spider_client.select_all(sql1)
        links = [data.get("link") for data in datas]
        dupfields = ["1004_{}".format(link) for link in links]




        pass

