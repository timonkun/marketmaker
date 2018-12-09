# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
挂单深度数据生产者：从主流交易所获取数据，并发送给消费者。
虚拟币刷单，要求在指定价格区间内波动，实现思路：基准值+浮动值，浮动值由主流币映射到价格波动区间内。
比如指定价格区间为0.3~0.5rmb，那么基准值=0.3rmb，浮动值[0, 0.2]，将eos的价格映射到[0, 0.2的区间]
"""
import time
from bitfinex import BitfinexExchange
from binance import BinanceExchange
from huobipro import HuobiExchange
from datetime import datetime


class VirtualProductor():
    def __init__(self, queue, symbol, exchange, currency_rate, price_min, price_max):
        self.queue = queue
        self.symbol = symbol    # 主流币,浮动参照
        if exchange == 'binance':
            self.source_exchange = BinanceExchange()
        elif exchange == 'bitfinex':
            self.source_exchange = BitfinexExchange()
        elif exchange == 'huobi':
            self.source_exchange = HuobiExchange()
        self.price_min = float(price_min) / currency_rate
        self.price_max = float(price_max) / currency_rate
        self.price_diff = self.price_max - self.price_min
        self.coef = 10 / self.price_diff  # 浮动值


    # 浮动参照eos，最近3个月价格在10usd以内,[0, 10] --> [0, 0.019]
    def price_mapping(self, base_price):
        float_price = abs(float(base_price) - 5) / self.coef
        price = self.price_min + float_price
        print ('base_price=%f, coef=%f, float_price=%f, price=%f' % (base_price, self.coef, float_price, price))
        return price

    def amount_mapping(self, base_amount):
        float_amount = float(base_amount)   # * self.coef
        return float_amount

    def fetch_order_book(self):
        order_book = self.source_exchange.fetch_order_book('EOS/USDT', 20)
        bids = order_book['bids']  # 买方，用户看到的卖价
        asks = order_book['asks']  # 卖方，用户看到的买价
        order_book_new = []
        count = 0
        for b in bids:
            if count > 10:
                break
            price = self.price_mapping(b[0])
            amount = self.amount_mapping(b[1])
            bid_dict = {'symbol': self.symbol, 'side': 'buy', 'price': price, 'amount': amount}
            order_book_new.append(bid_dict)
            count += 1

        # 除了CNB，其它都要委托成交
        if self.symbol != 'CNB/USDT':
            count = 0
            for b in asks:
                if count > 10:
                    break
                price = self.price_mapping(b[0])
                amount = self.amount_mapping(b[1])
                ask_dict = {'symbol': self.symbol, 'side': 'sell', 'price': price, 'amount': amount}
                order_book_new.append(ask_dict)
                count += 1

            # 成交单，价格、数量相等
            trades = self.source_exchange.fetch_trades('EOS/USDT', None, 10)
            for t in trades:
                price = self.price_mapping(t['price'])
                amount = self.amount_mapping(t['amount'])
                bid_dict = {'symbol': self.symbol, 'side': 'buy', 'price': price, 'amount': amount}
                order_book_new.append(bid_dict)
                ask_dict = {'symbol': self.symbol, 'side': 'sell', 'price': price, 'amount': amount}
                order_book_new.append(ask_dict)

        return order_book_new

    def run(self):
        print('Virtual Provider run.', self.symbol, self.price_min, self.price_max)
        while True:
            try:
                order_book = self.fetch_order_book()
                self.queue.put(order_book, block=True, timeout=None)
                print ('=================================')
                # 休眠60s
                time.sleep(60)
            except Exception as e:
                print(e)
