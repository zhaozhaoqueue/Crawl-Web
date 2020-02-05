# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlingWebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    full_name = scrapy.Field()
    note = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    present_time = scrapy.Field()
    link = scrapy.Field()
