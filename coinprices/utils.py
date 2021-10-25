import pymongo
from scrapy.conf import settings

class MarketPairs(object):
    def __init__(self):
        self.market_pair_list = {}
        connection = pymongo.MongoClient(
            settings['REMOTE_MONGO_HOST'],
            settings['REMOTE_MONGO_PORT'],
            connect=False,
        )
        db = connection[settings['REMOTE_MONGO_DB_BASE']]
        self.collection = db[settings['REMOTE_MONGO_EXCHANGE_COLLECTION']]
        self.exchange_init()

        
    def exchange_init(self):    
        if self.market_pair_list == None or len(self.market_pair_list) == 0:
            
            data = self.collection.find()
            for i in data:
                exchange = i['exchange']
                exchange_pair = i['exchange_pair']
                if exchange not in self.market_pair_list:
                    self.market_pair_list[exchange] = exchange_pair
                    
                    
    def get_market_pair(self, exchange='huobipro'):
        if self.market_pair_list == None or len(self.market_pair_list) == 0:
            self.exchange_init()
        market_pair_requested_list = self.market_pair_list[exchange]
        
        return market_pair_requested_list
market_pair = MarketPairs()        
