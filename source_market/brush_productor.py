# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
交易数据生产者：从主流交易所获取数据，并发送给消费者。

"""
import time
from bitfinex import BitfinexExchange
from binance import BinanceExchange
from huobipro import HuobiExchange
from datetime import datetime


class BrushProductor():
    def __init__(self, queue, symbol, exchange, brush_money_per_min):
        self.queue = queue
        self.symbol = symbol
        self.brush_money_per_min = brush_money_per_min
        if exchange == 'binance':
            self.source_exchange = BinanceExchange()
        elif exchange == 'bitfinex':
            self.source_exchange = BitfinexExchange()
        elif exchange == 'huobi':
            self.source_exchange = HuobiExchange()


    def fetch_trades(self):
        trades = self.source_exchange.fetch_trades(self.symbol, None, 50)
        # 换算成usdt价格
        symbol = self.symbol.split('/')[0] + '/USDT'
        price = self.source_exchange.fetch_last_price(symbol)
        money = 0
        count = 0
        trades_flt = []
        for t in trades:
            money += float(t['amount']) * price
            trades_flt.append(t)
            count += 1
            if money > self.brush_money_per_min:    # 平均到每分钟的交易金额
                print self.symbol + ': count=' + str(count) + ', money=' + str(money)
                break

        return trades_flt

    def run(self):
        print('Provider run.', self.symbol)
        while True:
            try:
                trades = self.fetch_trades()
                self.queue.put(trades, block=True, timeout=None)
                print ('=================================')
                # 休眠60s
                time.sleep(30)
            except Exception as e:
                print(e)
                time.sleep(30)
