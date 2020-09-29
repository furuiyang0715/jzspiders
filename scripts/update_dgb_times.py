from base_spider import SpiderBase


def get_pubdate(link):
    """从link提取出时间字符"""
    pass


class DgbUpdate(SpiderBase):

    def start(self):
        sql = '''select id, Website from OriginSpiderAll where PubDatetime > '2020-09-30 15:30:00';'''
        self._spider_init()
        items = self.spider_client.select_all(sql)
        _map = {item.get('id'): get_pubdate(item.get("Website")) for item in items}
        '''
        {
        id1: pubdate1, 
        id2: pubdate2, 
        id3: pubdate3, 
        ...
        }
        
        UPDATE mytable
            SET myfield = CASE other_field
                WHEN 1 THEN 'value'
                WHEN 2 THEN 'value'
                WHEN 3 THEN 'value'
            END
        WHERE id IN (1,2,3) 
        '''


if __name__ == '__main__':
    DgbUpdate().start()


'''
select WebSite,  str_to_date(left(SUBSTRING_INDEX(WebSite, '/', -3), 9), '%Y/%m%d')  from OriginSpiderAll \
where OrgTableCode = 1034 and PubDatetime > '2020-09-30 15:30:00' limit 10 ;
select count(*) from OriginSpiderAll where OrgTableCode = 1034 and PubDatetime > '2020-09-30 15:30:00';
select str_to_date('2018/1105', '%Y/%m%d');
update  OriginSpiderAll set PubDatetime = str_to_date(left(SUBSTRING_INDEX(WebSite, '/', -3), 9), '%Y/%m%d') \
where OrgTableCode = 1034 and PubDatetime > '2020-09-30 15:30:00';

'''