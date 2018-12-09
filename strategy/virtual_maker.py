# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
做市商策略的执行者。
输入：symbol, ticker, order book
输出：调用目标交易所接口进行交易
"""
import traceback
import time
import sys
import threading
import Queue
from strategy.brush_trade import BrushTrade
from strategy.liquidity_trade import LiquidityTrade
from strategy.virtual_trade import VirtualTrade
from source_market.brush_productor import BrushProductor
from source_market.liquidity_productor import LiquidityProductor
from source_market.virtual_productor import VirtualProductor


class VirtualMaker():

    def __init__(self, symbol, exchange, brush_money_per_min, currency_rate, price_min, price_max):
        self.symbol = symbol
        self.source_exchange = exchange
        self.brush_money_per_min = brush_money_per_min
        self.currency_rate = currency_rate
        self.price_min = price_min
        self.price_max = price_max
        self.queue3 = Queue.Queue(3)

    def run(self):
        try:
            virtual_productor = VirtualProductor(self.queue3, self.symbol, self.source_exchange, self.currency_rate, self.price_min, self.price_max)
            t_virtual_productor = threading.Thread(target=virtual_productor.run)
            t_virtual_productor.setDaemon(True)
            t_virtual_productor.start()

            virtual_trader = VirtualTrade(self.queue3)
            t_virtual_trader = threading.Thread(target=virtual_trader.run)  # 线程启动的调用的方法是函数run
            t_virtual_trader.setDaemon(True)
            t_virtual_trader.start()

            while True:
                # 主线程还负责检测子线程的存活情况
                if not t_virtual_productor.is_alive():
                    print("t_virtual_productor线程异常退出")
                    sys.exit(1)
                if not t_virtual_trader.is_alive():
                    print("t_virtual_trader线程异常退出")
                    sys.exit(1)
                time.sleep(3)

        except Exception:
            print(traceback.format_exc())
