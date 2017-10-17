import scrapy


class GooglescholarSpider(scrapy.Spider):
    name = 'googlescholar'
    allowed_domains = ['scholar.google.com']
    start_urls = [
        'https://scholar.google.de/scholar?q=((%22deep+learning%22+OR+%22deep+neural+network%22+OR+%22state-of-the-art%22)+AND+(%22genre+recognition%22+OR+%22genre+classification%22))&hl=en&as_sdt=0,5'
    ]

    @staticmethod
    def parse_title(article):
        title_parts = [
            i for i in article.xpath('h3//text()').extract()
            if i.strip() != '[PDF]'
        ]
        return "".join(title_parts).strip()

    def parse(self, response):
        articles = response.xpath('//div[contains(@class, gs_ri)]/*[h3]')
        for article in articles:
            title = self.parse_title(article)
            import ipdb
            ipdb.set_trace()
