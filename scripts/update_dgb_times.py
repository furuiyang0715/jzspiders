'''
select WebSite,  str_to_date(left(SUBSTRING_INDEX(WebSite, '/', -3), 9), '%Y/%m%d')  from OriginSpiderAll \
where OrgTableCode = 1034 and PubDatetime > '2020-09-30 15:30:00' limit 10 ;
select count(*) from OriginSpiderAll where OrgTableCode = 1034 and PubDatetime > '2020-09-30 15:30:00';
select str_to_date('2018/1105', '%Y/%m%d');
update  OriginSpiderAll set PubDatetime = str_to_date(left(SUBSTRING_INDEX(WebSite, '/', -3), 9), '%Y/%m%d') \
where OrgTableCode = 1034 and PubDatetime > '2020-09-30 15:30:00';
'''


'''脚本说明： 
时间: 2020-09-30 
需求: 
（1）将标题统一改为“快讯” 
（2）将内容改为原来的标题, 涉及到字段类型的更新
（3) 已入库历史的批量 update, 增量流的调整。 
'''
