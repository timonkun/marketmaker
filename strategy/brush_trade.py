# coding=utf-8
"""
@author: Manson
date: 2018年9月03日
做市商策略：刷单策略。
只提供策略。
"""
import time
import Queue
from datetime import datetime
from target_market.exchange import TargetExchange
from target_market import account
import traceback

# 刷单
class BrushTrade():
    def __init__(self, queue):
        self.queue = queue
        self.amount = 0
        self.target_exchange = TargetExchange()

    def trade(self):
        try:
            trades = self.queue.get(block=True, timeout=20) #接收消息
        except Queue.Empty:
            print("Nothing to do!i will go home!")
            return

        try:
            symbol = ''
            for t in trades:
                symbol = t['symbol']
                self.target_exchange.create_deal_order(account.account_list[0], t['symbol'], t['side'], float(t['amount']), float(t['price']))
                self.amount += float(t['amount'])
                time.sleep(0.1)
            print("work finished! %s amount=%s %s" % (symbol, self.amount, datetime.now()))
            self.queue.task_done()  #完成一个任务
            res = self.queue.qsize()    #判断消息队列大小
            if res > 0:
                print("fuck!There are still %d tasks to do" % (res))
        except Exception:
            print(traceback.format_exc())
        return

    def run(self):
        print('BrushTrade run.')
        while True:
            try:
                self.trade()
                print ('=================================')
                # 休眠s
                time.sleep(5)
            except Exception:
                print(traceback.format_exc())
                time.sleep(5)
