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

class USDTSpider(Spider):
    name = 'usdt'
    
    start_urls = []
    headers = {
            "Accept": "application/json",
            "Accept-Encoding": "deflate, gzip",
            'X-CMC_PRO_API_KEY':'96b417c2-4ba7-4902-88c0-945319c52c3a'
        }
    
    cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=USDT'
    start_urls.append(cmc_url)
    

    def start_requests(self):
        try:
            yield Request(url = self.start_urls[0], headers = self.headers, callback=self.parse_thread)
        except ex:
            print(ex)
        
        
    def parse_thread(self, response):
        if response is None:
            return
        r_usdt = bs(response.text)
        r_usdt = r_usdt.find("p").text
        if r_usdt is None or r_usdt == '':
            return
        try:
            json_data = json.loads(r_usdt)
            latest_price = json_data['data']['USDT']['quote']['USD']['price']
            ratio = json_data['data']['USDT']['quote']['USD']['percent_change_24h']
            Item = CoinPricesItem()
            Item["exchange"] = settings['CMC']
            Item["symbol"] = 'usdtusdt'
            Item["price"] = latest_price
            Item["ratio_24h"] = ratio
            Item["width_24h"] = 0
            Item["timestamp"] = int(time.time())
            yield Item
        except ex:
            print(ex)