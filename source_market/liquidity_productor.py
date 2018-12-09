# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
挂单深度数据生产者：从主流交易所获取数据，并发送给消费者。

"""
import time
from bitfinex import BitfinexExchange
from binance import BinanceExchange
from huobipro import HuobiExchange
from datetime import datetime

import time
from bitfinex import BitfinexExchange
from binance import BinanceExchange
from huobipro import HuobiExchange
from datetime import datetime


class LiquidityProductor():
    def __init__(self, queue, symbol, exchange):
        self.queue = queue
        self.symbol = symbol
        if exchange == 'binance':
            self.source_exchange = BinanceExchange()
        elif exchange == 'bitfinex':
            self.source_exchange = BitfinexExchange()
        elif exchange == 'huobi':
            self.source_exchange = HuobiExchange()


    def fetch_order_book(self):
        order_book = self.source_exchange.fetch_order_book(self.symbol, 20)
        bids = order_book['bids']  # 买方，用户看到的卖价
        asks = order_book['asks']  # 卖方，用户看到的买价
        order_book_new = []
        count = 0
        # 深度单
        for b in bids:
            if count > 10:
                break
            bid_dict = {'symbol': self.symbol, 'side': 'buy', 'price': b[0], 'amount': b[1]}
            order_book_new.append(bid_dict)
            count += 1

        count = 0
        for b in asks:
            if count > 10:
                break
            ask_dict = {'symbol': self.symbol, 'side': 'sell', 'price': b[0], 'amount': b[1]}
            order_book_new.append(ask_dict)
            count += 1

        # 成交单，价格、数量相等
        trades = self.source_exchange.fetch_trades(self.symbol, None, 10)
        for t in trades:
            bid_dict = {'symbol': self.symbol, 'side': 'buy', 'price': t['price'], 'amount': t['amount']}
            order_book_new.append(bid_dict)
            ask_dict = {'symbol': self.symbol, 'side': 'sell', 'price': t['price'], 'amount': t['amount']}
            order_book_new.append(ask_dict)

        return order_book_new

    def run(self):
        print('Provider run.', self.symbol)
        while True:
            try:
                order_book = self.fetch_order_book()
                self.queue.put(order_book, block=True, timeout=None)
                print ('=================================')
                # 休眠60s
                time.sleep(60)
            except Exception as e:
                print(e)
                time.sleep(60)
