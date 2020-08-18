spiders_config = {
    # 表名[容器名]: [启动文件路径, 启动方式(间隔/定点), 启动参数, 增量标的字段, 爬虫中文简称
    "juchao_kuaixun": ['Juchaodaynews/jcspider.py', "interval", (5, "minutes"), "CREATETIMEJZ", '巨潮快讯'],

    "juchao_info": ['Juchaodaynews/juchao_info.py', "interval", (10, "minutes"), "CREATETIMEJZ", '巨潮AI资讯'],

    "EEONews": ['EEOFinance/eeospider.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '经济观察网'],

    "9666pinglun": ['CN966/9666pinglun.py', 'interval', (10, "minutes"), "CREATETIMEJZ", '牛仔网评论'],

    'cctvfinance': ['CCTVFinance/cctv_spider.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '央视网财经'],

    'p2peye_news': ['P2Peye/p2peyespider.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '网贷天眼查'],

    'NewsYicai': ['YiCai/yicai_spider.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '第一财经'],

    'Takungpao': ['Takungpao/takungpao_main.py', 'interval', (15, 'minutes'), "CREATETIMEJZ", '大公报'],

    'SohuFinance': ['sohu/sohu_spider.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '搜狐财经'],

    'jfinfo': ['JfInfo/jfinfo_main.py', 'interval', (10, 'minutes'), "CREATETIMEJZ", '巨丰财经'],

    'stcn_info': ['StockStcn/kuaixun.py', 'interval', (11, 'minutes'), "CREATETIMEJZ", '证券时报网'],

    'cn_stock': ['ShangHaiSecuritiesNews/cn_main.py', 'interval', (9, 'minutes'), "CREATETIMEJZ", '上海证券报'],

    'netease_money': ['Money163/netease_money.py', 'interval', (9, 'minutes'), "CREATETIMEJZ", '网易财经'],

    'cls_telegraphs': ['ClsCnInfo/telegraphs.py', 'interval', (9, 'minutes'), "CREATETIMEJZ", '财新社-电报'],

    'gov_stats': ['GovSpiders/gov_main.py', 'interval', (2, 'days'), "CREATETIMEJZ", '国家统计局'],

    'chinabank': ['GovSpiders/gov_main.py', 'interval', (2, 'days'), "CREATETIMEJZ", '中国银行'],

    'qq_Astock_news': ['QQStock/qq_stock.py', 'interval', (9, 'minutes'), "CREATETIMEJZ", '腾讯财经[A股]'],

    'eastmoney_carticle': ['CArticle/ca_main.py', 'interval', (6, 'hours'), "CREATETIMEJZ", '东财财富号'],

}
