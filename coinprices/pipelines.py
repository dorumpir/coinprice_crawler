# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class CoinPricesPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['REMOTE_MONGO_HOST'],
            settings['REMOTE_MONGO_PORT'],
        )
        db = connection[settings['REMOTE_MONGO_DB']]
        self.collection = db[settings['REMOTE_MONGO_COIN_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{}'.format(data))
        if valid:
            self.collection.insert({"exchange": item.get("exchange"), 
            "symbol": item.get("symbol"), 
            "price": item.get("price"),
            "ratio_24h": item.get("ratio_24h"),
            "width_24h": item.get("width_24h"),
            "timestamp": item.get("timestamp")})
            log.msg('added to mongodb database', level=log.DEBUG, spider=spider)
        return item