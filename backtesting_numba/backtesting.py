from backtesting_numba.data_class import DataClass
import numpy as np
from numba import njit, prange, jit  # noqa
import time


# @njit(parallel=True, cache=True)
def backtesting_numba(
        op, hi, lo, cl,
        be, bc,
        se, sc,
        c_enter, c_exit, s_enter, s_exit,
        bsl, bsl_atr, bsl_value,
        btp, btp_atr, btp_value,
        bts, bts_atr, bts_value,
        ssl, ssl_atr, ssl_value,
        stp, stp_atr, stp_value,
        sts, sts_atr, sts_value,
        revert, signal,
        atr, atr_bool
):
    short_long = np.zeros(len(op))
    buy_enter_price = np.zeros(len(op))
    sell_enter_price = np.zeros(len(op))
    buy_exit_price = np.zeros(len(op))
    sell_exit_price = np.zeros(len(op))
    stop_loss_level = np.zeros(len(op))
    take_profit_level = np.zeros(len(op))
    traling_stop_level = np.zeros(len(op))
    stop_loss, take_profit, trailing_stop, price_enter, price_exit = [0] * 5
    price_exit = 0

    for i in prange(len(op)):

        if atr_bool and not atr[i]:
            continue

        if signal == 1:
            if take_profit and take_profit <= hi[i]:
                price_exit = take_profit - (c_exit + s_exit)
            if stop_loss and stop_loss >= lo[i]:
                price_exit = stop_loss - (c_exit + s_exit)
            if trailing_stop and trailing_stop >= lo[i]:
                price_exit = take_profit - (c_exit + s_exit)
            if (stop_loss and stop_loss >= lo[i]) and (trailing_stop and trailing_stop >= lo[i]):
                price_exit = max(stop_loss, trailing_stop) - (c_exit + s_exit)
            if bc[i] and bc[i] >= max(stop_loss, trailing_stop):
                price_exit = bc[i] - (c_exit + s_exit)

            if price_exit:
                signal = 0
                buy_exit_price[i] = price_exit
                price_exit, stop_loss, trailing_stop, take_profit = [0]*4
                continue

            if revert and se[i]:
                signal = -1
                buy_exit_price[i] = se[i] - (c_exit + s_exit)
                sell_enter_price[i] = price_enter
                if bsl:
                    stop_loss = price_enter - bsl_value
                    if bsl_atr:
                        stop_loss = price_enter - bsl_value * atr[i - 1]
                stop_loss_level[i] = stop_loss
                if btp:
                    take_profit = price_enter + btp_value
                    if btp_atr:
                        take_profit = price_enter + btp_value * atr[i - 1]
                take_profit_level[i] = take_profit
                if bts:
                    trailing_stop = price_enter - bts_value
                    if bts_atr:
                        trailing_stop = price_enter - bts_value * atr[i - 1]
                traling_stop_level[i] = trailing_stop
                # sell_exit
                if take_profit and take_profit >= lo[i]:
                    price_exit = take_profit + (c_exit + s_exit)
                if sc[i]:
                    price_exit = sc[i] + (c_exit + s_exit)
                if (take_profit and take_profit >= lo[i]) and sc[i]:
                    price_exit = max(sc[i], trailing_stop) - (c_exit + s_exit)
                if stop_loss and stop_loss <= hi[i]:
                    price_exit = stop_loss + (c_exit + s_exit)
                if trailing_stop and trailing_stop <= hi[i]:
                    price_exit = trailing_stop + (c_exit + s_exit)
                if (stop_loss and stop_loss <= hi[i]) and (trailing_stop and trailing_stop <= hi[i]):
                    price_exit = min(trailing_stop, stop_loss) + (c_exit + s_exit)
                if price_exit:
                    signal = 0
                    sell_exit_price[i] = price_exit
                    price_exit = stop_loss, trailing_stop, take_profit = [0]*4

            short_long[i] = signal

        if signal == -1:
            sell_enter_price[i] = 0
            sell_exit_price[i] = cl[i]
            signal = 0
            short_long[i] = signal
            continue

        if be[i] and se[i]:
            continue

        if be[i]:
            signal = 1
            price_enter = be[i] + (c_enter + s_enter)
            buy_enter_price[i] = price_enter
            # buy_levels
            if bsl:
                stop_loss = price_enter - bsl_value
                if bsl_atr:
                    stop_loss = price_enter - bsl_value * atr[i - 1]
            stop_loss_level[i] = stop_loss
            if btp:
                take_profit = price_enter + btp_value
                if btp_atr:
                    take_profit = price_enter + btp_value * atr[i - 1]
            take_profit_level[i] = take_profit
            if bts:
                trailing_stop = price_enter - bts_value
                if bts_atr:
                    trailing_stop = price_enter - bts_value * atr[i - 1]
            traling_stop_level[i] = trailing_stop
            # buy_exit
            if take_profit and take_profit <= hi[i]:
                price_exit = take_profit - (c_exit + s_exit)
            if bc[i]:
                price_exit = bc[i] - (c_exit + s_exit)
            if (take_profit and take_profit <= hi[i]) and bc[i]:
                price_exit = min(bc[i], trailing_stop) - (c_exit + s_exit)
            if stop_loss and stop_loss >= lo[i]:
                price_exit = stop_loss - (c_exit + s_exit)
            if trailing_stop and trailing_stop >= lo[i]:
                price_exit = trailing_stop - (c_exit + s_exit)
            if (stop_loss and stop_loss >= lo[i]) and (trailing_stop and trailing_stop >= lo[i]):
                price_exit = max(trailing_stop, stop_loss) - (c_exit + s_exit)
            if price_exit:
                signal = 0
                buy_exit_price[i] = price_exit
                price_exit, stop_loss, trailing_stop, take_profit = [0]*4
            short_long[i] = signal

        if se[i]:
            signal = -1
            price_enter = se[i] - (c_enter + s_enter)
            sell_enter_price[i] = price_enter
            # sell_levels
            if ssl:
                stop_loss = price_enter + ssl_value
                if ssl_atr:
                    stop_loss = price_enter + bsl_value * atr[i - 1]
            stop_loss_level[i] = stop_loss
            if stp:
                take_profit = price_enter - stp_value
                if stp_atr:
                    take_profit = price_enter - stp_value * atr[i - 1]
            take_profit_level[i] = take_profit
            if sts:
                trailing_stop = price_enter + sts_value
                if sts_atr:
                    trailing_stop = price_enter + sts_value * atr[i - 1]
            traling_stop_level[i] = trailing_stop
            # sell_exit
            if take_profit and take_profit >= lo[i]:
                price_exit = take_profit + (c_exit + s_exit)
            if sc[i]:
                price_exit = sc[i] + (c_exit + s_exit)
            if (take_profit and take_profit >= lo[i]) and sc[i]:
                price_exit = max(sc[i], trailing_stop) - (c_exit + s_exit)
            if stop_loss and stop_loss <= hi[i]:
                price_exit = stop_loss + (c_exit + s_exit)
            if trailing_stop and trailing_stop <= hi[i]:
                price_exit = trailing_stop + (c_exit + s_exit)
            if (stop_loss and stop_loss <= hi[i]) and (trailing_stop and trailing_stop <= hi[i]):
                price_exit = min(trailing_stop, stop_loss) + (c_exit + s_exit)
            if price_exit:
                signal = 0
                sell_exit_price[i] = price_exit
                price_exit = stop_loss, trailing_stop, take_profit = [0]*4
            short_long[i] = signal

    return short_long, buy_enter_price, sell_enter_price, buy_exit_price, sell_exit_price, \
        stop_loss_level, take_profit_level, traling_stop_level


class Backtesting:

    def __init__(self, data_class, index_date=False, with_indicators=False):
        """
        :param data_class: DataClass object
        """

        if not isinstance(data_class, DataClass):
            try:
                data_class = DataClass(data_class, index_date=index_date, with_indicators=with_indicators)
            except Exception as e:
                print('cold not convert data into DataClass, see DataClass documentation')
                raise e

        self.data_class = data_class

    def indicator(self, func, *args, **kwargs):
        try:
            indicators = func(self.data_class, *args, **kwargs)
            for key, value in indicators.items():
                self.data_class.add_update_indicator(key, value)
        except Exception as e:
            raise e

    def buy_enter(self, func, *args, **kwargs):
        try:
            buy_enter = func(self.data_class, *args, **kwargs)
            self.data_class._set_buy_enter(buy_enter)
        except Exception as e:
            raise e

    def buy_close(self, func, *args, **kwargs):
        try:
            buy_close = func(self.data_class, *args, **kwargs)
            self.data_class._set_buy_close(buy_close)
        except Exception as e:
            raise e

    def sell_enter(self, func, *args, **kwargs):
        try:
            sell_enter = func(self.data_class, *args, **kwargs)
            self.data_class._set_sell_enter(sell_enter)
        except Exception as e:
            raise e

    def sell_close(self, func, *args, **kwargs):
        try:
            sell_close = func(self.data_class, *args, **kwargs)
            self.data_class._set_sell_close(sell_close)
        except Exception as e:
            raise e

    def backtesting(
            self,
            comission_enter=0, comission_exit=0, slippage_enter=0, slippage_exit=0,
            buy_stop_loss=False, bsl_atr=False, bsl_value=2,
            buy_take_profit=False, btp_atr=False, btp_value=2,
            buy_trailing_stop=False, bts_atr=False, bts_value=2,
            sell_stop_loss=False, ssl_atr=False, ssl_value=2,
            sell_take_profit=False, stp_atr=False, stp_value=2,
            sell_trailing_stop=False, sts_atr=False, sts_value=2,
            revert=False, signal=0,
            timeit=False
    ):
        time1 = time.time()
        len_data = len(self.data_class.dataframe)

        if self.data_class.buy_enter is None:
            self.data_class.buy_enter = np.zeros(len_data)

        if self.data_class.buy_close is None:
            self.data_class.buy_close = np.zeros(len_data)

        if self.data_class.sell_enter is None:
            self.data_class.sell_enter = np.zeros(len_data)

        if self.data_class.sell_close is None:
            self.data_class.sell_close = np.zeros(len_data)

        atr_bool = False
        avarange_true_range = np.zeros(len_data)

        if any([bsl_atr, btp_atr, bts_atr, ssl_atr, stp_atr, sts_atr]):
            if 'atr' not in self.data_class.indicators.keys():
                print('For use any atr=True please set a "atr" indicator in data_class')
                raise ValueError

            avarange_true_range = self.data_class.indicators['atr']

        short_long, enter_price, exit_price, stop_loss_level, take_profit_level, traling_stop_level = \
            backtesting_numba(
                self.data_class.open, self.data_class.high, self.data_class.low, self.data_class.close,
                self.data_class.buy_enter, self.data_class.buy_close,
                self.data_class.sell_enter, self.data_class.sell_close,
                comission_enter, comission_exit, slippage_enter, slippage_exit,
                buy_stop_loss, bsl_atr, bsl_value,
                buy_take_profit, btp_atr, btp_value,
                buy_trailing_stop, bts_atr, bts_value,
                sell_stop_loss, ssl_atr, ssl_value,
                sell_take_profit, stp_atr, stp_value,
                sell_trailing_stop, sts_atr, sts_value,
                revert, signal,
                avarange_true_range, atr_bool
            )

        dict_indicators = {
            'short_long': short_long,
            'enter_price': enter_price,
            'exit_price': exit_price,
            'stop_loss_level': stop_loss_level,
            'take_profit_level': take_profit_level,
            'traling_stop_level': traling_stop_level,
        }

        for key, value in dict_indicators.items():
            self.data_class.add_update_indicator(key, value)

        time2 = time.time()
        if timeit:
            print('function took {:.3f} ms'.format((time2 - time1) * 1000.0))
