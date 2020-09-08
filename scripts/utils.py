# https://shimo.im/sheet/GhgYXDg3xJRWY6G8/s3E4K

org_tablecode_map = {
    "juchao_kuaixun": ['巨潮快讯', 1060, ],

    "juchao_info": ['巨潮 AI 资讯', 1012, ],

    "EEONews": ['经济观察网', 1045, ],

    "9666pinglun": ['牛仔网评论', 1046, ],

    'cctvfinance': ['央视网财经', 1043, ],

    'p2peye_news': ['网贷天眼查', 1051, ],

    'NewsYicai': ['第一财经', 1024, ],

    'Takungpao': ['大公报', 1034],

    'SohuFinance': ['搜狐财经', 1022, ],

    'jfinfo': ['巨丰财经', 1033, ],

    'stcn_info': ['证券时报网', 1011, ],

    'cn_stock': ['上海证券报', 1009, ],

    'netease_money': ['网易财经滚动新闻', 1025, ],

    'cls_telegraphs': ['财新社[电报]', 1029, ],

    'gov_stats': ['国家统计局', 1061, ],

    'chinabank': ['中国银行', 1062, ],

    'qq_Astock_news': ['腾讯财经[A股]', 1023, ],

    'eastmoney_carticle': ['东财财富号', 1004, ],

    'securities_daily_latest': ['证券日报[最新播报]', 1075, ],

    'xueqiu_livenews': ['雪球快讯', 1074, ],

    'taoguba': ['淘股吧', 1006, ]

}


''' UNIQUE KEY `date_title` (`pub_date`,`title`),
(1) 巨潮快讯 
select code as SecuCode, name as SecuAbbr, pub_date as PubDatetime, \
title as Title, type as InnerType, link as Website, CREATETIMEJZ, UPDATETIMEJZ \
from juchao_kuaixun limit 10 \G


'''
