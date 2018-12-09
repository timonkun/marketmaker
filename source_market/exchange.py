# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
交易所通用类封装，查询各个交易所不同币种的ticker, order book。
输入参数：exchange和symbol
输出结果：ticker, order book
"""


import pandas as pd
from time import sleep

# base_coin = symbol.split('/')[-1]
# trade_coin = symbol.split('/')[0]

class Exchange():

    def __init__(self, exchange):
        self.exchange = exchange            # 交易所

    def fetch_ticker(self, symbol):
        # 获取最新的卖出价格
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker

    def fetch_trades(self, symbol, since, limit):
        trades = self.exchange.fetch_trades(symbol, since=since, limit=limit)
        return trades

    def fetch_order_book(self, symbol, limit):
        # 根据交易对查询订单信息
        order_book = self.exchange.fetch_order_book(symbol=symbol, limit=limit)  # limit参数控制返回最近的几条
        return order_book

    #print t['info']

# 获取最新的买入价格
#price = exchange.fetch_ticker(symbol)['ask']  # 获取卖一价格