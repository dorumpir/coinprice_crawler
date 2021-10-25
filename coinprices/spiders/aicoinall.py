from scrapy.spider import Spider
from scrapy.http import Request
from bs4 import BeautifulSoup as bs
import requests
import time
from datetime import datetime
import json
import re
from scrapy.conf import settings
from ..items import CoinPricesItem
from ..utils import market_pair

global market_pair
class ExchangeSpider(Spider):
    name = 'aicoin'
    aicoin_ids = ['huobipro', 'okex', 'zb', 'gate', 'binance', 'bitmex', 'coinex', 'liqui', 'bibox', 'bitfinex', 'bittrex', ]

    def start_requests(self):
        aicoin_pairs = dict()
        for aicoin_id in self.aicoin_ids:
            aicoin_pairs[aicoin_id] = market_pair.get_market_pair(aicoin_id)
        start_urls = []
        for aicoin_id, exchange_pairs in aicoin_pairs.items():
            for coinpair in exchange_pairs:
                coinpair = coinpair.replace('_','').lower()
                if coinpair.endswith('usdt'):
                    # interval: 5min = 300s, frame_24h = 24h * 60 min / 5min = 288
                    url = "https://widget.aicoin.net.cn/chart/api/data/period?symbol=%s%s&step=%s" % (aicoin_id, coinpair, '300')
                    yield Request(url=url, callback=lambda response, exchange=aicoin_id, symbol=coinpair: self.parse_thread(response,exchange,symbol))

    @staticmethod
    def cal_ratio(open_price, close_price):
        return (close_price - open_price) / close_price * 100

    @staticmethod
    def cal_width(series):
        width = max(series) - min(series)
        return width
        
    def parse_thread(self, response, exchange, symbol):
        rtext = bs(response.text)
        rtext = rtext.find("p").text
        latest_price = 0
        ratio = 0.0
        width = 0.0
        price_period = []
        Item = CoinPricesItem()
        #print(rtext)
        json_data = json.loads(rtext)
        latest_price_list = json_data.get("data")
        if latest_price_list:
            
            latest_price = latest_price_list[-1][4]
            
            price_period.append([x[4] for x in latest_price_list])
            data_288 = price_period[-288:]
            open_price = data_288[0][1]
            close_price = data_288[-1][4]
            ratio = self.cal_ratio(open_price=open_price, close_price=close_price)
            series = [x[2] for x in data_288] + [y[3] for y in data_288]
            width = self.cal_width(series=series)
        if not latest_price_list:
            pass
            
        Item["exchange"] = exchange
        Item["symbol"] = symbol
        Item["price"] = latest_price
        Item["ratio_24h"] = ratio
        Item["width_24h"] = width
        Item["timestamp"] = int(time.time())
        yield Item
