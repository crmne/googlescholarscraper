import re
import scrapy

from googlescholar.items import Article


class GooglescholarSpider(scrapy.Spider):
    name = 'googlescholar'
    allowed_domains = ['scholar.google.de']
    start_urls = [
        'https://scholar.google.de/scholar?q=((%22deep+learning%22+OR+%22deep+neural+network%22+OR+%22state-of-the-art%22)+AND+(%22genre+recognition%22+OR+%22genre+classification%22))&hl=en&as_sdt=0,5'
    ]

    @staticmethod
    def parse_title(article):
        title_parts = [
            i for i in article.xpath('h3//text()').extract()
            if i.strip() not in [
                '[PDF]', '[CITATION]', '[C]', '[CITATION][C]', '[HTML]',
                '[DOC]', '[DOC][DOC]'
            ]
        ]
        return "".join(title_parts).strip()

    def parse(self, response):
        articles = response.xpath('//div[contains(@class, gs_ri)]/*[h3]')
        for article_dom in articles:
            article = Article()
            article['title'] = self.parse_title(article_dom)

            link = article_dom.xpath('h3/a/@href')
            if link:
                article['link'] = link.extract()[0]

            description = "".join([
                i.replace('\xa0', '')
                for i in article_dom.xpath(
                    'div[contains(@class, gs_a)]//text()').extract()
            ])

            authors_journal = description.split('-')
            if len(authors_journal) > 0:
                article['authors'] = description.split('-')[0].strip()
            if len(authors_journal) > 1:
                journal = description.split('-')[1].strip()
                year = re.match(r"(\d+)", journal.split(', ')[-1])

                if year:
                    article['journal'] = journal
                    article['year'] = int(year.group(0))
            yield article

        next_page = response.xpath('//a[b[text() = "Next"]]/@href')
        if next_page:
            url = response.urljoin(next_page.extract()[0])
            yield scrapy.Request(url, callback=self.parse)
