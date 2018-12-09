# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
binance交易所实例。
输入参数：
输出结果：
"""

import ccxt
from exchange import Exchange
from source_market import apikey
from datetime import datetime
import time


class BinanceExchange():
    def __init__(self):
        self.exchange = ccxt.binance()  # 创建交易所，此处为okex交易所
        self.exchange.apiKey = apikey.binance_apiKey_ro  # 此处加上自己的apikey和secret，都需要开通交易权限
        self.exchange.secret = apikey.binance_secret_ro
        self.source_exchange = Exchange(self.exchange)

    def fetch_ticker(self, symbol):
        return self.source_exchange.fetch_ticker(symbol)

    def fetch_trades(self, symbol, since, limit):
        trades = self.source_exchange.fetch_trades(symbol, since=since, limit=limit)
        return trades

    def fetch_last_price(self, symbol):
        ticker = self.source_exchange.fetch_ticker(symbol)
        return float(ticker['info']['lastPrice'])

    def fetch_order_book(self, symbol, limit):
        return self.source_exchange.fetch_order_book(symbol, limit)


# symbol_btc = 'BTC/USDT'  # 交易品种
#
# bian_exchange = BinanceExchange()
# order_book = bian_exchange.fetch_order_book(symbol_btc, 20)
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
# ticker = bian_exchange.fetch_ticker(symbol_btc)
# print ticker['info']['lastPrice']
# trades = bian_exchange.fetch_trades(symbol_btc, None, 10)
# for t in trades:
#     print  t['symbol'], t['price'], t['amount'], t['side']
