# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GooglescholarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    journal = scrapy.Field()
    year = scrapy.Field()
    description = scrapy.Field()
    pdflink = scrapy.Field()
    link = scrapy.Field()
    biblink = scrapy.Field()
