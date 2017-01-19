# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SoftJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Author = scrapy.Field()
    DateTime = scrapy.Field()
    IP = scrapy.Field()
    Content = scrapy.Field()
    Comment = scrapy.Field()
    Score = scrapy.Field()
    Url = scrapy.Field()
