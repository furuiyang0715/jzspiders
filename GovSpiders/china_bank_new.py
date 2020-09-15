from GovSpiders.base_spider import GovBaseSpider


class ChinaBankNew(GovBaseSpider):

    def __init__(self):
        super(ChinaBankNew, self).__init__()
        self.index_url = 'http://www.pbc.gov.cn/'

    def start(self):
        page = self.js_get_page(self.index_url)
        print(page)


if __name__ == '__main__':
    ChinaBankNew().start()
    pass
