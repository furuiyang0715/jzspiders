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
            'CreateTime',  # 创建时间
            'UpdateTime',   # 更新时间
        ]

    def _create_table(self):
        """创建汇总表"""
        sql = '''
        CREATE TABLE `OriginSpiderAll` (
          `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
          `PubDatetime` datetime NOT NULL COMMENT '发布时间(精确到秒)',
          `MedName` varchar(50) NOT NULL COMMENT '资讯来源（网站名称）',
          `Title` varchar(1000) NOT NULL COMMENT '标题',
          `Website` varchar(1000) DEFAULT NULL COMMENT '网址',
          `OrgTableCode` varchar(50) NOT NULL COMMENT '资讯原始来源代码',
          `OrgID` bigint(20) unsigned NOT NULL COMMENT '资讯原始来源表id',
          `OrgMedName` varchar(50) NOT NULL COMMENT '资讯来源（原始-一般在详情页标题下方）',
          `Abstract` varchar(1000) DEFAULT NULL COMMENT '摘要(有的网站有摘要这个字段，如有则写，没有就留空)',
          `Content` longtext DEFAULT NULL COMMENT '资讯文章正文',
          `DetailString` longtext NOT NULL COMMENT '明细字符串(可用程序转化为dict格式)',
          `IfRepeat` tinyint(4) NOT NULL DEFAULT 0 COMMENT '是否重复(默认0，0-不重复，1重复)',
          `IsValid` tinyint(4) NOT NULL DEFAULT 1 COMMENT '是否有效。0-无效；1-有效',
          `CMFTime` datetime NOT NULL COMMENT '资讯原始来源表入库时间(以内容写入时间为准)',
          `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
          `UpdateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `unified_key1` (`OrgTableCode`, `OrgID`) USING BTREE,
          UNIQUE KEY `unified_key2` (`Website`) USING BTREE,
          KEY `key` (`PubDatetime`, `MedName`, `OrgTableCode`, `OrgID`, `OrgMedName`, `UpdateTime`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='爬虫数据源表'; 
        '''

        fields = [
            'id',  # 自增 ID
            'PubDatetime',    # 对应于网站的发布时间 pub_date
            'MedName',  # 资讯来源，网站名称，类似于 "巨潮快讯"、"财联社" 等 ...
            'Title',  # 文章标题，对应于分表中的 title
            'Website',  # 网址，对应于分表中的 link
            'OrgTableCode',  # 资讯原始来源代码 在 https://shimo.im/sheet/GhgYXDg3xJRWY6G8/s3E4K 中找对应
            'OrgID',  # 资讯原始来源表 ID   去除该字段 ////
            'OrgMedName',  # 资讯原始来源
            'Abstract',  # 摘要，可为空
            'Content',   # 资讯文章正文
            'DetailString',    # 明细字符串 去除该字段 ////
            'IfRepeat',   # 是否重复 去除该字段 ////
            'IsValid',  # 是否有效 去除该字段  ////
            'CMFTime',  # 资讯原始来源表入库时间 去除该字段 ////
            'CreateTime',  # 创建时间
            'UpdateTime',   # 更新时间
        ]

        sql2 = '''
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
          `CreateTime` datetime DEFAULT CURRENT_TIMESTAMP,
          `UpdateTime` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          UNIQUE KEY `unified_key1` (`OrgTableCode`) USING BTREE,
          UNIQUE KEY `unified_key2` (`Website`) USING BTREE,
          KEY `key` (`PubDatetime`, `MedName`, `OrgTableCode`, `OrgMedName`, `UpdateTime`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='原始爬虫数据汇总表';  
        '''

        self.spider_client.insert(sql2)
        self.spider_client.end()

    def show_create_table(self, table):
        sql = '''select * from {} limit 1; '''.format(table)
        info = self.spider_client.select_one(sql)
        if info:
            self.fields.extend(list(info.keys()))

    def start(self):
        self._create_table()
        # for table in self.tables:
        #     self.show_create_table(table)
        # print(set(self.fields))

        pass


if __name__ == '__main__':
    merge = MergeHistory()
    merge.start()
