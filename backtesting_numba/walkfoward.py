from backtesting_numba.backtesting import Backtesting
import types


class WalkFoward:

    indicator_func = None
    inperiod = 0
    outperiod = 0

    walkfoward_dataframe = None

    def __init__(
            self, backtesting, inperiod, outperiod, indicator_main_function,
            buy_enter_function=False, sell_enter_function=False, buy_exit_function=False, sell_exit_function=False,
            comission_enter=0, comission_exit=0, slippage_enter=0, slippage_exit=0,
            buy_stop_loss=False, bsl_atr=False, bsl_value=2,
            buy_take_profit=False, btp_atr=False, btp_value=2,
            buy_trailing_stop=False, bts_atr=False, bts_value=2,
            sell_stop_loss=False, ssl_atr=False, ssl_value=2,
            sell_take_profit=False, stp_atr=False, stp_value=2,
            sell_trailing_stop=False, sts_atr=False, sts_value=2,
            revert=False, fitness_function=False,
    ):

        if not isinstance(backtesting, Backtesting):
            print('backtesting is not a Backtesting object')
            raise ValueError

        if not isinstance(indicator_main_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(indicator_main_function)}')
            raise ValueError

        if not isinstance(buy_enter_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(buy_enter_function)}')
            raise ValueError

        if not isinstance(sell_enter_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(sell_enter_function)}')
            raise ValueError

        if not isinstance(sell_exit_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(sell_exit_function)}')
            raise ValueError

        if not isinstance(buy_exit_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(buy_exit_function)}')
            raise ValueError

        if not isinstance(fitness_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(fitness_function)}')
            raise ValueError

        self.backtesting = backtesting
        self.inperiod = inperiod
        self.outperiod = outperiod
        self.indicator_main_function = indicator_main_function
        self.buy_enter_function = buy_enter_function
        self.sell_enter_function = sell_enter_function
        self.buy_exit_function = buy_exit_function
        self.sell_exit_function = sell_exit_function
        self.fitness_function = fitness_function
        self.revert = revert
        self.sts_value = sts_value
        self.sts_atr = sts_atr
        self.sell_trailing_stop = sell_trailing_stop
        self.stp_value = stp_value
        self.stp_atr = stp_atr
        self.sell_take_profit = sell_take_profit
        self.ssl_value = ssl_value
        self.ssl_atr = ssl_atr
        self.sell_stop_loss = sell_stop_loss
        self.bts_value = bts_value
        self.bts_atr = bts_atr
        self.buy_trailing_stop = buy_trailing_stop
        self.btp_value = btp_value
        self.btp_atr = btp_atr
        self.buy_take_profit = buy_take_profit
        self.bsl_atr = bsl_atr
        self.bsl_value = bsl_value
        self.buy_stop_loss = buy_stop_loss
        self.slippage_exit = slippage_exit
        self.slippage_enter = slippage_enter
        self.comission_exit = comission_exit
        self.comission_enter = comission_enter

    def run_walkfoward(self, *args, **kwargs):
        df = self.backtesting.data_class.dataframe.copy

        max_indicator_global = 0
        for key, value in kwargs.items():
            try:
                iter(value)
            except TypeError:
                print(f'All values in **kwargs must be interable, the {key} value is not interable')

            for item in value:
                if not isinstance(item, int):
                    print(f'all kwargs in the function must be the type int, the the '
                          f'key={key}, value={value}, item={item} you give is not int')
                if item <= 0:
                    print(f'all kwargs must be bigger than one the '
                          f'key={key}, value={value}, item={item} you give is negative')
                    raise ValueError

                max_indicator_global = item if item > max_indicator_global else max_indicator_global

        dc_indices = {}

        in_start = len(df) - self.inperiod - self.outperiod
        out_start = len(df) - self.outperiod
        out_end = len(df)
        n = 0

        while in_start - max_indicator_global >= 0:
            dc_indices[n] = [in_start, out_start, out_end]
            n += 1
            in_start -= self.outperiod
            out_start -= self.outperiod
            out_end -= self.outperiod

        return dc_indices