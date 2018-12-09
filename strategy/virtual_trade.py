# coding=utf-8
"""
@author: Manson
date: 2018年9月06日
做市商策略：做市策略，提供流动性。
只提供策略。
"""
import time
import Queue
from datetime import datetime
from target_market.exchange import TargetExchange
from target_market import account
import traceback
import random

# 先把源交易所的深度搬过来
class VirtualTrade():
    def __init__(self, queue):
        self.queue = queue
        self.amount = 0
        self.target_exchange = TargetExchange()
        self.account_index = 0

    def trade(self):
        try:
            order_book = self.queue.get(block=True, timeout=10) #接收消息
        except Queue.Empty:
            print("Nothing to do!i will go home!")
            return

        if len(order_book) == 0:
            print ("order_book is null, Nothing to do! i will go home!")
            return
        symbol = order_book[0]['symbol']

        # 10个账号，轮询使用，先取消前一个账号的订单，再下当前账号新订单，依次往复循环。
        account_cur = account.account_list[self.account_index]
        if self.account_index == 0:
            last_index = len(account.account_list) - 1
        else:
            last_index = self.account_index - 1
        account_last = account.account_list[last_index]
        print ("account_index=%d, last_index=%d, account_cur=%d, account_last=%d " % (self.account_index, last_index, account_cur, account_last))
        self.account_index += 1
        self.account_index = self.account_index % len(account.account_list)

        try:
            # 获取未成交订单，并取消，可以替换成一个取消所有订单接口
            response = self.target_exchange.get_open_orders(account_last, symbol, -1)
            if response is not None:
                json_data = response.json()
                if json_data['state'] == '1':
                    orders = json_data['data']['order_info']
                    for o in orders:
                        self.target_exchange.cancel_order(account_last, symbol, o['id'])

            # 下新订单
            for b in order_book:
                self.target_exchange.create_limit_order(account_cur, b['symbol'], b['side'], float(b['amount']), float(b['price']))
                self.amount += float(b['amount'])
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
        print('VirtualTrade run.')
        while True:
            try:
                self.trade()
                print ('=================================')
                # 休眠s
                time.sleep(5)
            except Exception:
                print(traceback.format_exc())
                time.sleep(5)