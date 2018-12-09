# -*- coding: utf-8 -*-
"""
@author: Manson
date: 2018年09月03日
目标交易所接口类封装
"""
import requests
import url_config, account
import json
import traceback

class TargetExchange():
    def __init__(self):
        return

    # 直接成交接口，刷单用。
    def create_deal_order(self, uid, symbol, side, amount, price):
        url = '%s?u_no=%s&symbol=%s&side=%s&amount=%s&price=%s' % (
            url_config.add_order_url, uid, symbol, side, amount, price)
        try:
            response = requests.post(url, data=None, headers=url_config.form_header, verify=True)
            if len(response.content) > 0:
                print url, response.text.encode('utf-8')
            return response
        except Exception:
            print(traceback.format_exc())

    # 委托限价单接口
    def create_limit_order(self, uid, symbol, side, amount, price):
        url = '%s?u_no=%s&symbol=%s&side=%s&amount=%s&price=%s' % (
            url_config.add_trade_url, uid, symbol, side, amount, price)
        try:
            response = requests.post(url, data=None, headers=url_config.form_header, verify=True)
            if len(response.content) > 0:
                print url, response.text.encode('utf-8')
            return response
        except Exception:
            print(traceback.format_exc())

    # 根据id获取订单
    def get_order(self, uid, symbol, order_id):
        action = 'fetch_order'
        url = '%s?u_no=%s&symbol=%s&action=%s&id=%s' % (
            url_config.order_url, uid, symbol, action, order_id)
        try:
            response = requests.post(url, data=None, headers=url_config.form_header, verify=True)
            if len(response.content) > 0:
                print url, response.text.encode('utf-8')
            return response
        except Exception:
            print(traceback.format_exc())

    # 获取未成交订单
    def get_open_orders(self, uid, symbol, limit):
        action = 'fetch_open_orders'
        url = '%s?u_no=%s&symbol=%s&action=%s&limit=%s' % (
            url_config.order_url, uid, symbol, action, limit)
        try:
            response = requests.post(url, data=None, headers=url_config.form_header, verify=True)
            if len(response.content) > 0:
                print url, response.text.encode('utf-8')
            return response
        except Exception:
            print(traceback.format_exc())

    # 取消订单
    def cancel_order(self, uid, symbol, order_id):
        action = 'cancel_order'
        url = '%s?u_no=%s&symbol=%s&action=%s&id=%s' % (
            url_config.order_url, uid, symbol, action, order_id)
        try:
            response = requests.post(url, data=None, headers=url_config.form_header, verify=True)
            if len(response.content) > 0:
                print url, response.text.encode('utf-8')
            return response
        except Exception:
            print(traceback.format_exc())


#237878735&symbol=ETH/BTC&side=buy&amount=0.13&price=7380
if __name__ == "__main__":
    symbol = 'ETH/USDT'
    #account = account.account_list[0]
    try:
        target_exchange = TargetExchange()
        #target_exchange.create_deal_order(account.account1, 'ETH/BTC', 'buy', 0.13, 7301)
        # response = target_exchange.create_limit_order(account, symbol, 'buy', 4000, 0.0398)
        # json_data = response.text
        # print json_data
        # order_id = json_data['data']['order_info']['id']     # 多了个空格
        # print order_id
        # response = target_exchange.cancel_order(account.account1, 'ETH/BTC', order_id)

        # response = target_exchange.get_order(account, symbol, 340667)
        # print response.text
        #
        for i in range (0, 10):
            response = target_exchange.get_open_orders(account.account_list[i], symbol, -1)
            print response.text
            json_data = response.json()
            orders = json_data['data']['order_info']
            print len(orders)
            for o in orders:
                if o['status'] == 'open':
                    print o
                    response = target_exchange.cancel_order(account.account_list[i], symbol, o['id'])
                    print response.text


        # response = target_exchange.get_order(account.account1, 'ETH/BTC', json_data['data']['order_info']['id'])
        # print response.text

    except Exception:
        print(traceback.format_exc())
