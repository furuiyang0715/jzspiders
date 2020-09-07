"""完成历史数据的汇总"""
from base_spider import SpiderBase
from spiders_cfg import spiders_config


class MergeHistory(SpiderBase):
    def __init__(self):
        super(MergeHistory, self).__init__()
        self.tables = list(spiders_config.keys())
        self._spider_init()
        self.fields = [
            'id',  # 自增 ID
            'PubDatetime',    # 对应于网站的发布时间 pub_date
            'MedName',  # 资讯来源，网站名称，类似于 "巨潮快讯"、"财联社" 等 ...
            'Title',  # 文章标题，对应于分表中的 title
            'Website',  # 网址，对应于分表中的 link
            'OrgTableCode',  # 资讯原始来源代码 在 https://shimo.im/sheet/GhgYXDg3xJRWY6G8/s3E4K 中找对应
            'OrgMedName',  # 资讯原始来源
            'Abstract',  # 摘要，可为空
            'Content',   # 资讯文章正文
            'SecuCode',    # 相关股票代码
            'SecuAbbr',   # 相关股票简称
            'InnerType',  # 内部资讯类别
            'KeyWords',  # 文章关键词
            'DupField',  # 去重标志字段
            'CreateTime',  # 创建时间
            'UpdateTime',   # 更新时间
        ]

    def _create_table(self):
        """创建汇总表"""
        sql = '''
        CREATE TABLE IF NOT EXISTS `OriginSpiderAll` (
          `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
          `PubDatetime` datetime NOT NULL COMMENT '发布时间(精确到秒)',
          `MedName` varchar(50) NOT NULL COMMENT '资讯来源（网站名称）',
          `Title` varchar(1000) NOT NULL COMMENT '标题',
          `Website` varchar(1000) DEFAULT NULL COMMENT '网址',
          `OrgTableCode` varchar(50) NOT NULL COMMENT '资讯原始来源代码',
          `OrgMedName` varchar(50) NOT NULL COMMENT '资讯来源（原始-一般在详情页标题下方）',
          `Abstract` varchar(1000) DEFAULT NULL COMMENT '摘要(有的网站有摘要这个字段，如有则写，没有就留空)',
          `Content` longtext DEFAULT NULL COMMENT '资讯文章正文',
          `SecuCode` varchar(8) DEFAULT NULL COMMENT '证券代码',
          `SecuAbbr` varchar(16) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '证券简称',
          `InnerType` varchar(16) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '内部资讯类别', 
          `KeyWords` varchar(64) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '文章关键词', 
          `DupField` varchar(20) NOT NULL COMMENT '资讯去重依据', 
          `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
          `UpdateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `unified_key1` (`OrgTableCode`) USING BTREE,
          UNIQUE KEY `unified_key2` (`DupField`) USING BTREE,
          KEY `key` (`PubDatetime`, `MedName`, `OrgTableCode`, `OrgMedName`, `UpdateTime`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='原始爬虫数据汇总表';  
        '''

        self.spider_client.insert(sql)
        self.spider_client.end()

    # def show_create_table(self, table):
    #     sql = '''select * from {} limit 1; '''.format(table)
    #     info = self.spider_client.select_one(sql)
    #     if info:
    #         self.fields.extend(list(info.keys()))

    def start(self):
        self._create_table()

        pass


if __name__ == '__main__':
    merge = MergeHistory()
    merge.start()
