import os
import re

import scrapy
from dotenv import find_dotenv, load_dotenv

from googlescholar.items import Article


class GooglescholarSpider(scrapy.Spider):
    name = 'googlescholar'
    allowed_domains = ['scholar.google.com']

    def __init__(self, category=None, *args, **kwargs):
        super(GooglescholarSpider, self).__init__(*args, **kwargs)

        dotenv_file = find_dotenv()
        if dotenv_file:
            load_dotenv(dotenv_file)

        self.query = os.environ['QUERY']
        self.start_urls = [
            'https://scholar.google.com/scholar?q={}'.format(self.query)
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
        if 'Server Error' in response.body.decode():
            raise scrapy.exceptions.IgnoreRequest(
                'Server Error. Trying next page')
            url = re.sub(r'start=(\d+)',
                         lambda x: "start={}".format(int(x.group(1)) + 10),
                         response.url)
            yield scrapy.Request(url, callback=self.parse)

        if "Please show you're not a robot" in response.body.decode():
            raise scrapy.exceptions.CloseSpider('Identified as robot')

        articles = response.xpath('//div[contains(@class, gs_ri)]/*[h3]')
        for article_selector in articles:
            article = Article()
            article['title'] = self.parse_title(article_selector)

            link = article_selector.xpath('h3/a/@href')
            if link:
                article['link'] = link.extract()[0]

            description = "".join([
                i.replace('\xa0', '')
                for i in article_selector.xpath(
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
