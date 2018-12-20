# coding=utf-8
"""
@author: Manson
date: 2018年10月09日
按照设计好的K线数据刷成交单
"""
import sys
sys.path.append('/opt/quant/marketmaker')
import pandas as pd
from datetime import datetime, timedelta
from time import sleep
from target_market.exchange import TargetExchange
from target_market import account
from random import random


pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# 1. 读取表格K线，开始循环
# 2. 每个整点周期运行一次函数
# 3. 首先刷开盘价的成交单，中间分别刷最高价和最低价，最后刷收盘价的成交单，交易量平均分配在各个单里
# 4. 结束

# sleep
def next_run_time(time_interval, ahead_time=1):

    if time_interval.endswith('m'):
        now_time = datetime.now()
        time_interval = int(time_interval.strip('m'))

        target_min = (int(now_time.minute / time_interval) + 1) * time_interval
        if target_min < 60:
            target_time = now_time.replace(minute=target_min, second=0, microsecond=0)
        else:
            if now_time.hour == 23:
                target_time = now_time.replace(hour=0, minute=0, second=0, microsecond=0)
                target_time += timedelta(days=1)
            else:
                target_time = now_time.replace(hour=now_time.hour + 1, minute=0, second=0, microsecond=0)

        # sleep直到靠近目标时间之前
        if (target_time - datetime.now()).seconds < ahead_time+1:
            print('Not far from target_time=', ahead_time, 's, wait for next-next loop.')
            target_time += timedelta(minutes=time_interval)
        print('Next run time>>> ', target_time)
        return target_time
    else:
        exit('time_interval doesn\'t end with m')


def random_side():
    count = random()
    if count < 0.5:
        return 'buy'
    else:
        return 'sell'


if __name__ == "__main__":
    time_interval = '5m'  # 间隔运行时间
    has_exception_occur = False
    target_exchange = TargetExchange()  # 交易所
    symbol = 'CNB/USDT'    # 交易对

    # 账号
    account1 = account.account_list[0]
    # =====导入EOSUSD每一天的5分钟数据
    df = pd.read_csv(
        '../statistics/5MIN_CNBUSDT.csv')
       # skiprows=1)
    print df
    last_close_price = 0
    while True:
        for i in range(df.shape[0]):
            # if i < 144:
            #     continue
            # ===sleep直到运行时间
            run_time = next_run_time(time_interval)
            if not has_exception_occur:
                sleep(max(0, (run_time - datetime.now()).seconds))
            while True:  # 在靠近目标时间时
                if datetime.now() < run_time and not has_exception_occur:
                    continue
                else:
                    break

            sleep(1)

            open_price = round(float(df.at[i,'open']), 5)
            high_price = round(float(df.at[i, 'high']), 5)
            low_price = round(float(df.at[i, 'low']), 5)
            close_price = round(float(df.at[i, 'close']), 5)
            float_price = round(random() * (high_price - low_price)/2, 5)
            if last_close_price>0:
                open_price = last_close_price
            coef = 1
            if random() < 0.5:
                coef = -1
            close_price += round(coef * float_price, 5)
            high_price -= round(float_price/2, 5)
            low_price += round(float_price/2, 5)
            last_close_price = close_price
            volume = round(float(df.at[i, 'volume']), 4) + round(random() * 1000, 2)
            print(df.at[i, 'index'], open_price, high_price, low_price, close_price, volume)
            total_volume = 0
            total_second = 0

            trade_volume = round(random() * 500, 2)
            total_volume += trade_volume
            # 开盘价成交单
            side = random_side()
            target_exchange.create_deal_order(account1, symbol, side, trade_volume, open_price)
            sleep(1)

            # 当交易量未达到设定值，并且时间不满4分钟的时候，持续循环交易
            while (total_volume < volume) and (total_second < 3.5*60):
                gap_second = round(random() * 5, 1)  # 1~10
                trade_volume = round(random() * (volume/40), 2)  # 1~1000
                float_price = round(random() * (high_price-low_price), 5)   # 0.001~0.01

                # 浮动价成交单
                side = random_side()
                target_exchange.create_deal_order(account1, symbol, side, trade_volume, low_price + float_price)
                sleep(gap_second)

                total_volume += trade_volume
                total_second += gap_second
                print (total_volume, volume, total_second)

            # 最高价成交单
            trade_volume = round(random() * 1000, 2)
            side = random_side()
            target_exchange.create_deal_order(account1, symbol, side, trade_volume, high_price)
            sleep(1)

            # 最低价成交单
            trade_volume = round(random() * 1000, 2)
            side = random_side()
            target_exchange.create_deal_order(account1, symbol, side, trade_volume, low_price)
            sleep(1)
            # 收盘价成交单
            trade_volume = round(random() * 500, 2)
            side = random_side()
            target_exchange.create_deal_order(account1, symbol, side, trade_volume, close_price)
            sleep(1)
            for i in range(0,5):
                # 收盘价成交单
                trade_volume = round(random() * 500, 2)
                target_exchange.create_deal_order(account1, symbol, 'buy', trade_volume, close_price)
                # 收盘价成交单
                trade_volume = round(random() * 500, 2)
                target_exchange.create_deal_order(account1, symbol, 'sell', trade_volume, close_price)