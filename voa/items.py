# -*- coding: utf-8 -*-


import scrapy


class VoaItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    imageUrl = scrapy.Field()
    categoryId = scrapy.Field()
