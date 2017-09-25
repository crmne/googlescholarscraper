import scrapy


class GooglescholarSpider(scrapy.Spider):
    name = 'googlescholar'
    allowed_domains = ['scholar.google.com']
    start_urls = [
        'https://scholar.google.de/scholar?q=((%22deep+learning%22+OR+%22deep+neural+network%22+OR+%22state-of-the-art%22)+AND+(%22genre+recognition%22+OR+%22genre+classification%22))&hl=en&as_sdt=0,5'
    ]

    def parse(self, response):
        with open('test.html', 'wb') as f:
            f.write(response.body)
