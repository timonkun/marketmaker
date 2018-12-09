# -*- coding: utf-8 -*-
"""
@author: Manson
date: 2018年09月03日
程序入口
"""
import traceback
import time
import sys
import threading
from strategy.virtual_maker import VirtualMaker
from config import source_exchange, symbol_list_virtual, brush_money_per_min_per_variety, currency_rate


if __name__ == "__main__":
    try:
        # 使用locals()生成动态变量，节省代码量
        for i in range(0, symbol_list_virtual.__len__()):
            locals()['market_maker_'+str(i)] = VirtualMaker(symbol_list_virtual[i]['symbol'], source_exchange, brush_money_per_min_per_variety,
                                                            currency_rate, symbol_list_virtual[i]['price_min'], symbol_list_virtual[i]['price_max'])
            locals()['t_market_maker_' + str(i)] = threading.Thread(target=locals()['market_maker_'+str(i)].run)
            locals()['t_market_maker_' + str(i)].setDaemon(True)
            locals()['t_market_maker_' + str(i)].start()
            time.sleep(1)

        while True:
            # 主线程还负责检测子线程的存活情况
            for i in range(0, symbol_list_virtual.__len__()):
                if not locals()['t_market_maker_' + str(i)].is_alive():
                    print("t_market_maker线程异常退出")
                    sys.exit(1)
            time.sleep(1)

    except Exception:
        print(traceback.format_exc())
