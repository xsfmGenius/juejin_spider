# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SegmentfaultspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    up = scrapy.Field()
    read = scrapy.Field()
    reputation = scrapy.Field()
    time = scrapy.Field()
    followA = scrapy.Field()
    Afollow = scrapy.Field()
    loc = scrapy.Field()
    company = scrapy.Field()
    introduce = scrapy.Field()
