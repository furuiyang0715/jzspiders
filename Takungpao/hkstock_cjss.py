from lxml import html
from Takungpao.base import TakungpaoBase


class HKStock_CJSS(TakungpaoBase):
    def __init__(self):
        super(HKStock_CJSS, self).__init__()
        self.page = 2
        self.type = '财经时事'
        self.first_url = 'http://finance.takungpao.com/hkstock/cjss/index.html'
        self.format_url = "http://finance.takungpao.com/hkstock/cjss/index_{}.html"

    def _parse_detail(self, body):
        result = self.extractor.extract(body)
        content = result.get("content")
        return content

    def parse_list(self, body):
        items = []
        doc = html.fromstring(body)
        news_list = doc.xpath("//div[@class='m_txt_news']/ul/li")
        # print(news_list)
        # print(len(news_list))
        for news in news_list:
            item = {}
            title = news.xpath("./a[@class='a_title']")
            if not title:
                title = news.xpath("./a[@class='a_title txt_blod']")
            title = title[0].text_content()
            # print(title)
            item['title'] = title
            pub_date = news.xpath("./a[@class='a_time txt_blod']")
            if not pub_date:
                pub_date = news.xpath("./a[@class='a_time']")

            link = pub_date[0].xpath("./@href")[0]
            # print(link)
            item['link'] = link

            pub_date = pub_date[0].text_content()
            # print(pub_date)
            item['pub_date'] = pub_date
            items.append(item)

            detail_resp = self.get(link)
            if detail_resp and detail_resp.status_code == 200:
                article = self._parse_detail(detail_resp.text)
                if article:
                    article = self._process_content(article)
                    item['article'] = article
                    # print(item)
        return items

    def start(self):
        self._create_table()
        self._spider_init()
        for page in range(1, self.page+1):
            if page == 1:
                list_url = self.first_url
            else:
                list_url = self.format_url.format(page)

            list_resp = self.get(list_url)
            if list_resp and list_resp.status_code == 200:
                items = self.parse_list(list_resp.text)
                page_save_num = self._batch_save(self.spider_client, items, self.table_name, self.fields)
                print(f"第{page}页保存成功的个数{page_save_num}")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def _parse_list(self, body):
        items = []
        doc = html.fromstring(body)
        news_list = doc.xpath("//div[@class='m_txt_news']/ul/li")
        for news in news_list:
            item = dict()
            title = news.xpath("./a[@class='a_title']")
            if not title:
                title = news.xpath("./a[@class='a_title txt_blod']")
            title = title[0].text_content()
            item['Title'] = title
            pub_date = news.xpath("./a[@class='a_time txt_blod']")
            if not pub_date:
                pub_date = news.xpath("./a[@class='a_time']")

            link = pub_date[0].xpath("./@href")[0]
            item['Website'] = link
            pub_date = pub_date[0].text_content()
            item['PubDatetime'] = pub_date
            items.append(item)

            detail_resp = self.get(link)
            if detail_resp and detail_resp.status_code == 200:
                article = self._parse_detail(detail_resp.text)
                if article:
                    article = self._process_content(article)
                    item['Content'] = article
                    # 新增合并字段
                    item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                    item['MedName'] = self.name
                    if not item.get('OrgMedName'):
                        item['OrgMedName'] = self.name
                    item['OrgTableCode'] = self.table_code
                    self._save(self.spider_client, item, self.merge_table, self.merge_fields)

    def run(self):
        self._spider_init()
        for page in range(1, self.page + 1):
            if page == 1:
                list_url = self.first_url
            else:
                list_url = self.format_url.format(page)
            print(list_url)
            list_resp = self.get(list_url)
            if list_resp and list_resp.status_code == 200:
                self._parse_list(list_resp.text)


class HKStock_QQGS(HKStock_CJSS):
    def __init__(self):
        super(HKStock_QQGS, self).__init__()
        self.type = '全球股市'
        self.first_url = 'http://finance.takungpao.com/hkstock/qqgs/index.html'
        self.format_url = "http://finance.takungpao.com/hkstock/qqgs/index_{}.html"


class HKStock_JJYZ(HKStock_CJSS):
    def __init__(self):
        super(HKStock_JJYZ, self).__init__()
        self.type = '经济一周'
        self.first_url = 'http://finance.takungpao.com/hkstock/jjyz/index.html'
        self.format_url = "http://finance.takungpao.com/hkstock/jjyz/index_{}.html"


class HKStock_JGSD(HKStock_CJSS):
    def __init__(self):
        super(HKStock_JGSD, self).__init__()
        self.type = '机构视点'
        self.first_url = 'http://finance.takungpao.com/hkstock/jgsd/index.html'
        self.format_url = "http://finance.takungpao.com/hkstock/jgsd/index_{}.html"


class HKStock_GSYW(HKStock_CJSS):
    def __init__(self):
        super(HKStock_GSYW, self).__init__()
        self.type = '公司要闻'
        self.first_url = 'http://finance.takungpao.com/hkstock/gsyw/index.html'
        self.format_url = "http://finance.takungpao.com/hkstock/gsyw/index_{}.html"


class HKStock_GJJJ(HKStock_CJSS):
    def __init__(self):
        super(HKStock_GJJJ, self).__init__()
        self.type = '国际聚焦'
        self.first_url = 'http://finance.takungpao.com/hkstock/gjjj/index.html'
        self.format_url = "http://finance.takungpao.com/hkstock/gjjj/index_{}.html"


if __name__ == '__main__':
    HKStock_CJSS().run()

    HKStock_QQGS().run()

    HKStock_JJYZ().run()

    HKStock_JGSD().run()

    HKStock_GSYW().run()

    HKStock_GJJJ().run()

    pass
