# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CoinPricesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    exchange = Field()
    symbol = Field()
    price = Field()
    ratio_24h = Field()
    width_24h = Field()
    timestamp = Field()
    pass
