from lxml import html
from Takungpao.base import TakungpaoBase


class FK(TakungpaoBase):
    def __init__(self):
        super(FK, self).__init__()
        self.list_url = 'http://finance.takungpao.com/fk/'
        self.type = '风口'

    def _parse_detail(self, body):
        result = self.extractor.extract(body)
        content = result.get("content")
        return content

    def start(self):
        self._create_table()
        self._spider_init()
        resp = self.get(self.list_url)
        if resp and resp.status_code == 200:
            body = resp.text
            doc = html.fromstring(body)
            news_list = doc.xpath('//div[@class="wrap-l js-list fl_dib"]/ul/li/div[@class="list-text fr_dib"]')
            items = []
            for news in news_list:
                item = {}
                title = news.xpath('./h1/a')[0].text_content()
                item['title'] = title
                link = news.xpath('./h1/a/@href')[0]
                item['link'] = link
                pub_date = news.xpath('./div[@class="date"]')[0].text_content()
                item['pub_date'] = pub_date
                detail_resp = self.get(link)
                if detail_resp and detail_resp.status_code == 200:
                    detail_page = detail_resp.text
                    article = self._parse_detail(detail_page)
                    if article:
                        item['article'] = article
                        # print(item)
                        items.append(item)

            fk_save_num = self._batch_save(self.spider_client, items, self.table_name, self.fields)
            print("风口保存的个数是 {}".format(fk_save_num))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def run(self):
        self._spider_init()
        resp = self.get(self.list_url)
        if resp and resp.status_code == 200:
            body = resp.text
            doc = html.fromstring(body)
            news_list = doc.xpath('//div[@class="wrap-l js-list fl_dib"]/ul/li/div[@class="list-text fr_dib"]')
            for news in news_list:
                item = {}
                title = news.xpath('./h1/a')[0].text_content()
                item['Title'] = title
                link = news.xpath('./h1/a/@href')[0]
                item['Website'] = link
                pub_date = news.xpath('./div[@class="date"]')[0].text_content()
                item['PubDatetime'] = pub_date
                detail_resp = self.get(link)
                if detail_resp and detail_resp.status_code == 200:
                    detail_page = detail_resp.text
                    article = self._parse_detail(detail_page)
                    if article:
                        item['Content'] = article
                        # 新增合并字段
                        item['DupField'] = "{}_{}".format(self.table_code, item['Website'])
                        item['MedName'] = self.name
                        if not item.get('OrgMedName'):
                            item['OrgMedName'] = self.name
                        item['OrgTableCode'] = self.table_code
                        self._save(self.spider_client, item, self.merge_table, self.merge_fields)


if __name__ == '__main__':
    # FK().start()

    FK().run()

    pass
