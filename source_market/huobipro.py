# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
huobipro交易所实例。
输入参数：
输出结果：
"""

import ccxt
from exchange import Exchange
from source_market import apikey


class HuobiExchange():
    def __init__(self):
        self.exchange = ccxt.huobipro()  # 创建交易所
        self.exchange.apiKey = apikey.huobi_apiKey_ro  # 此处加上自己的apikey和secret，都需要开通交易权限
        self.exchange.secret = apikey.huobi_secret_ro
        self.source_exchange = Exchange(self.exchange)

    def fetch_ticker(self, symbol):
        return self.source_exchange.fetch_ticker(symbol)

    def fetch_trades(self, symbol, since, limit):
        trades = self.source_exchange.fetch_trades(symbol, since=since, limit=limit)
        return trades

    def fetch_last_price(self, symbol):
        ticker = self.source_exchange.fetch_ticker(symbol)
        return float(ticker['last'])

    def fetch_order_book(self, symbol, limit):
        return self.source_exchange.fetch_order_book(symbol, limit)


 # amount = float(t['info']['amount'])
            # price = float(t['info']['price'])
            # side = t['info']['type']
            # symbol = t['symbol']

# symbol_btc = 'BTC/USDT'  # 交易品种
#
# huobi_exchange = HuobiExchange()
# order_book = huobi_exchange.fetch_order_book(symbol_btc, 10)
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
# ticker = huobi_exchange.fetch_ticker(symbol_btc)
# print ticker['last']
# trades = huobi_exchange.fetch_trades(symbol_btc, None, 10)
# for t in trades:
#     #date = datetime.fromtimestamp(t['info']['timestamp'])
#     print t

