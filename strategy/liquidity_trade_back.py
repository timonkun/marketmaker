# coding=utf-8
"""
@author: Manson
date: 2018年9月06日
做市商策略：做市策略，提供流动性。
只提供策略。
"""
import time
import copy
import traceback

class LiquidityTrade():
    def __init__(self):
        return

    # 价格趋势系数
    def price_trend_factor(self, trades, buy1_price, sell1_price, buy2_price, sell2_price, buy3_price, sell3_price,
                           vol_list, index_type=None, symmetric=True):
        prices = trades["price"].values.tolist()
        latest_trades = prices[-6:]
        mid_price = (buy1_price + sell1_price) / 2 * 0.7 + (buy2_price + sell2_price) / 2 * 0.2 + (
                    buy3_price + sell3_price) / 2 * 0.1
        latest_trades.append(mid_price)
        is_bull_trend = False
        is_bear_trend = False
        last_price_too_far_from_latest = False
        has_large_vol_trade = False

        if latest_trades[-1] > max(latest_trades[:-1]) + latest_trades[-1] * 0.00005 or (
                latest_trades[-1] > max(latest_trades[:-2]) + latest_trades[-1] * 0.00005 and latest_trades[-1] >
                latest_trades[-2]):
            is_bull_trend = True
        elif latest_trades[-1] < min(latest_trades[:-1]) - latest_trades[-1] * 0.00005 or (
                latest_trades[-1] < min(latest_trades[:-2]) - latest_trades[-1] * 0.00005 and latest_trades[-1] <
                latest_trades[-2]):
            is_bear_trend = True

        if abs(latest_trades[-1] - latest_trades[-2] * 0.7 - latest_trades[-3] * 0.2 - latest_trades[-4] * 0.1) > \
                latest_trades[-1] * 0.002:
            last_price_too_far_from_latest = True

        if max(vol_list) > 20:
            has_large_vol_trade = True

        if is_bull_trend or is_bear_trend or last_price_too_far_from_latest or has_large_vol_trade:
            return 0

        index = 50
        # if index_type == "rsi":
        #     prices = trades["price"]
        #     index = indicators.rsi_value(prices, len(prices) - 1)
        # else:
        #     index = self.buy_trades_ratio(trades)
        # 价格趋势严重，暂停交易
        if index <= 20 or index >= 80:
            return 0

        # 对称下单时，factor用来调整下单总数
        if symmetric:
            factor = 1 - abs(index - 50) / 50
        # 非对称下单时，factor用来调整买入订单的数量
        else:
            factor = index / 50
        return factor


    # 从最小价差向外挂单
    def orders_price_and_qty_from_min_spread(self, buy1_price, sell1_price, total_qty, price_step, qty_step,
                                             min_qty_per_order, max_qty_per_order, min_price_spread, buy_ratio=1,
                                             sell_ratio=1):
        orders_list = []
        remaining_qty = total_qty
        avg_price = (buy1_price + sell1_price) / 2

        if buy_ratio > 1:  # price is going down
            avg_price += 0.2
        elif sell_ratio > 1:  # price is going up
            avg_price -= 0.2

        buy_order_price = avg_price - min_price_spread / 2
        sell_order_price = avg_price + min_price_spread / 2
        order_qty = min(min_qty_per_order, remaining_qty)
        while remaining_qty >= min_qty_per_order and buy_order_price > buy1_price and sell_order_price < sell1_price:
            # buy_order_qty = max(order_qty * buy_ratio, self.min_order_qty)
            # sell_order_qty = max(order_qty * sell_ratio, self.min_order_qty)
            buy_order_qty = max(order_qty, self.min_order_qty)
            sell_order_qty = max(order_qty, self.min_order_qty)
            orders_list.append({"price": buy_order_price, "amount": buy_order_qty, "type": "buy"})
            orders_list.append({"price": sell_order_price, "amount": sell_order_qty, "type": "sell"})
            remaining_qty -= buy_order_qty
            buy_order_price -= price_step
            sell_order_price += price_step
            order_qty = min(buy_order_qty + qty_step, max_qty_per_order)
            order_qty = min(remaining_qty, order_qty)
        return orders_list


    # 做市算法下单功能
    def trade_thread(self):
        while True:
            try:
                if self.timeInterval > 0:
                    self.timeLog("Trade - 等待 %d 秒进入下一个循环..." % self.timeInterval)
                    time.sleep(self.timeInterval)

                # 检查order_info_list里面还有没有pending的order，然后cancel他们
                order_id_list = []
                for odr in self.order_info_list:
                    order_id_list.append(odr["order_id"])
                self.huobi_cancel_pending_orders(order_id_list=order_id_list)
                self.order_info_list = []

                account = self.get_huobi_account_info()

                buy1_price = self.get_huobi_buy_n_price()
                sell1_price = self.get_huobi_sell_n_price()
                buy2_price = self.get_huobi_buy_n_price(n=2)
                sell2_price = self.get_huobi_sell_n_price(n=2)
                buy3_price = self.get_huobi_buy_n_price(n=3)
                sell3_price = self.get_huobi_sell_n_price(n=3)

                buy1_vol = self.get_huobi_buy_n_vol()
                sell1_vol = self.get_huobi_sell_n_vol()
                buy2_vol = self.get_huobi_buy_n_vol(n=2)
                sell2_vol = self.get_huobi_sell_n_vol(n=2)
                buy3_vol = self.get_huobi_buy_n_vol(n=3)
                sell3_vol = self.get_huobi_sell_n_vol(n=3)
                buy4_vol = self.get_huobi_buy_n_vol(n=4)
                sell4_vol = self.get_huobi_sell_n_vol(n=4)
                buy5_vol = self.get_huobi_buy_n_vol(n=5)
                sell5_vol = self.get_huobi_sell_n_vol(n=5)

                vol_list = [buy1_vol, buy2_vol, buy3_vol, buy4_vol, buy5_vol, sell1_vol, sell2_vol, sell3_vol,
                            sell4_vol, sell5_vol]

                latest_trades_info = self.get_latest_market_trades()

                # 账户或者行情信息没有取到
                if not all([account, buy1_price, sell1_price]):
                    continue

                self.heart_beat_time.value = time.time()

                global init_account_info
                if init_account_info is None:
                    init_account_info = account

                global account_info_for_r_process
                account_info_for_r_process = copy.deepcopy(self.account_info)

                min_price_spread = self.arbitrage_min_spread(self.get_huobi_buy_n_price(), self.min_spread_rate)
                # 计算下单数量
                total_qty = min(self.total_qty_per_transaction, account.btc, account.cash / buy1_price)
                trend_factor = self.price_trend_factor(latest_trades_info, buy1_price, sell1_price, buy2_price,
                                                       sell2_price, buy3_price, sell3_price, vol_list,
                                                       symmetric=self.is_symmetric)
                if self.is_symmetric:
                    total_qty *= trend_factor
                    buy_ratio = 1
                    sell_ratio = 1
                else:
                    buy_ratio = trend_factor
                    sell_ratio = 2 - trend_factor
                order_data_list = self.orders_price_and_qty_from_min_spread(buy1_price, sell1_price, total_qty,
                                                                            self.price_step, self.qty_step,
                                                                            self.min_qty_per_order,
                                                                            self.max_qty_per_order,
                                                                            min_price_spread, buy_ratio=buy_ratio,
                                                                            sell_ratio=sell_ratio)
                self.spot_batch_limit_orders(self.market_type, order_data_list,
                                             time_interval_between_threads=self.time_interval_between_threads)
                current_spread = self.bid_ask_spread(self.exchange)
                self.save_transactions(signal_spread=current_spread, signal_side="market_maker")
                self.latest_trade_time = time.time()
            except Exception:
                print(traceback.format_exc())
                continue