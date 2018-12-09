# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
bitfinex交易所实例。
输入参数：
输出结果：
"""

import ccxt
from exchange import Exchange
from source_market import apikey
from datetime import datetime
import time


class BitfinexExchange():
    def __init__(self):
        self.exchange = ccxt.bitfinex()  # 创建交易所，此处为okex交易所
        self.exchange.apiKey = apikey.bitfinex_apiKey_ro  # 此处加上自己的apikey和secret，都需要开通交易权限
        self.exchange.secret = apikey.bitfinex_secret_ro
        self.source_exchange = Exchange(self.exchange)

    def fetch_ticker(self, symbol):
        return self.source_exchange.fetch_ticker(symbol)

    def fetch_trades(self, symbol, since, limit):
        trades = self.source_exchange.fetch_trades(symbol, since=since, limit=limit)
        for t in trades:
            t['symbol'] = t['symbol']
            t['price'] = t['info']['price']
            t['amount'] = t['info']['amount']
            t['side'] = t['info']['type']
        return trades

    def fetch_last_price(self, symbol):
        ticker = self.source_exchange.fetch_ticker(symbol)
        return float(ticker['info']['last_price'])

    def fetch_order_book(self, symbol, limit):
        return self.source_exchange.fetch_order_book(symbol, limit)


 # amount = float(t['info']['amount'])
            # price = float(t['info']['price'])
            # side = t['info']['type']
            # symbol = t['symbol']

# symbol_btc = 'BTC/USDT'  # 交易品种
#
# bfx_exchange = BitfinexExchange()
# order_book = bfx_exchange.fetch_order_book(symbol_btc, 10)
# bids = order_book['bids']   # 买方
# print 'bids:'
# for b in bids:
#     price = b[0]
#     amount = b[1]
#     print price, amount
# print '--------------------'
# print 'asks:'
# asks = order_book['asks']    # 卖方
# for a in asks:
#     price = a[0]
#     amount = a[1]
#     print price, amount
# ticker = bfx_exchange.fetch_ticker(symbol_btc)
# print ticker['info']['last_price']
# now = datetime.now()
# print now
# time = time.mktime(datetime.now().timetuple())
# print time
# trades = bfx_exchange.fetch_trades(symbol_btc, time, 10)
# for t in trades:
#     date = datetime.fromtimestamp(t['info']['timestamp'])
#     print date, t['info']

