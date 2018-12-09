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
from source_market.brush_productor import BrushProductor
from source_market.liquidity_productor import LiquidityProductor


class MarketMaker():

    def __init__(self, symbol, exchange, brush_money_per_min):
        self.symbol = symbol
        self.source_exchange = exchange
        self.brush_money_per_min = brush_money_per_min
        self.queue = Queue.Queue(3)

    def run(self):
        try:
            brush_productor = BrushProductor(self.queue, self.symbol, self.source_exchange, self.brush_money_per_min)
            t_brush_productor = threading.Thread(target=brush_productor.run)
            t_brush_productor.setDaemon(True)
            t_brush_productor.start()

            brush_trader = BrushTrade(self.queue)
            t_brush_trader = threading.Thread(target=brush_trader.run)     # 线程启动的调用的方法是函数run
            t_brush_trader.setDaemon(True)
            t_brush_trader.start()

            # liquidity_productor = LiquidityProductor(self.queue, self.symbol, self.source_exchange)
            # t_liquidity_productor = threading.Thread(target=liquidity_productor.run)
            # t_liquidity_productor.setDaemon(True)
            # t_liquidity_productor.start()
            #
            # liquidity_trader = LiquidityTrade(self.queue)
            # t_liquidity_trader = threading.Thread(target=liquidity_trader.run)  # 线程启动的调用的方法是函数run
            # t_liquidity_trader.setDaemon(True)
            # t_liquidity_trader.start()

            while True:
                # 主线程还负责检测子线程的存活情况
                if not t_brush_productor.is_alive():
                    print("t_provider线程异常退出")
                    sys.exit(1)
                if not t_brush_trader.is_alive():
                    print("t_brush_trader线程异常退出")
                    sys.exit(1)
                # if not t_liquidity_productor.is_alive():
                #     print("t_liquidity_productor线程异常退出")
                #     sys.exit(1)
                # if not t_liquidity_trader.is_alive():
                #     print("t_liquidity_trader线程异常退出")
                #     sys.exit(1)
                time.sleep(3)

        except Exception:
            print(traceback.format_exc())
            time.sleep(3)
