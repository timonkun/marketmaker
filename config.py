# -*- coding: utf-8 -*-
"""
@author: Manson
date: 2018年09月05日
配置文件
"""
from forex_python.converter import CurrencyRates

# 交易所和品种
# source_exchange = 'bitfinex'
# symbol_list = ['ETH/BTC', 'BTC/USDT', 'ETH/USDT']

# source_exchange = 'huobi'
# symbol_list = ['ETH/BTC', 'BTC/USDT', 'ETH/USDT']
#
source_exchange = 'binance'

symbol_list = ['LTC/USDT', 'ETH/USDT', 'BTC/USDT', 'LTC/BTC', 'ETH/BTC', 'LTC/ETH']
symbol_list_virtual = [#{'symbol': 'CNB/USDT', 'price_min': 0.289, 'price_max': 0.291},
                       {'symbol': 'GYB/USDT', 'price_min': 0.015, 'price_max': 0.023},
                       {'symbol': 'MTO/USDT', 'price_min': 0.021, 'price_max': 0.035},
                       {'symbol': 'ECH/USDT', 'price_min': 0.018, 'price_max': 0.028},
                       {'symbol': 'TCB/USDT', 'price_min': 0.012, 'price_max': 0.033}]

# 每天刷的资金量(美元)
# 按汇率6.8算，5亿cny约合7350万美元
# 获取汇率
cr = CurrencyRates()
currency_rate = cr.get_rates('USD')[u'CNY']

# 控制系数，用来对冲多的金额
coefficient = 0.95
brush_money_per_day = 500000000.0 * coefficient / currency_rate
brush_money_per_min = brush_money_per_day / (24*60)
brush_money_per_min_per_variety = brush_money_per_min / symbol_list.__len__()

print str(brush_money_per_min_per_variety) + ' usd'