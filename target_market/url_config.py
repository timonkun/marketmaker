# -*- coding: utf-8 -*-
"""
@author: Manson
date: 2018年09月03日
目标交易所接口类封装
"""

base_url = 'http://www.icb.group/api'

add_trade_url = base_url + '/add_trade.ashx'
add_order_url = base_url + '/add_order.ashx'
order_url = base_url + '/order.ashx'

json_header = {'content-type': "application/json"}
form_header = {'content-type': 'application/x-www-form-urlencoded', 'id': '123888' }
