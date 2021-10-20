from backtesting_numba.backtesting import Backtesting
from backtesting_numba.metrics_dataframe import result_return
from backtesting_numba.data_class import DataClass
from backtesting_numba.metrics_dataframe import dataframe_metrics
import types
import numpy as np
import pandas as pd


def wf_dataframe_signal_iend(DF, i_stop_calc):
    df = DF.copy()
    sr_signal = np.array(df.short_long)

    for i, signal in enumerate(sr_signal):
        if i == i_stop_calc and signal == 0:
            return 0, i_stop_calc
        elif i > i_stop_calc and signal != sr_signal[i - 1]:
            return signal, i

    return sr_signal[-1], len(df)


def empty_backtest(df, signal=0):
    back = Backtesting(df)

    back.backtesting(df, signal=signal)

    return back.data_class.dataframe


class WalkFoward:
    indicator_func = None
    inperiod = 0
    outperiod = 0

    df_final = None
    df_metrics = None

    trades_result = None
    return_result = None
    winrate_result = None

    def __init__(
            self, data, inperiod, outperiod, indicator_main_function=False,
            buy_enter_function=False, sell_enter_function=False, buy_exit_function=False, sell_exit_function=False,
            comission_enter=0, comission_exit=0, slippage_enter=0, slippage_exit=0,
            buy_stop_loss=False, bsl_atr=False, bsl_value=2,
            buy_take_profit=False, btp_atr=False, btp_value=2,
            buy_trailing_stop=False, bts_atr=False, bts_value=2,
            sell_stop_loss=False, ssl_atr=False, ssl_value=2,
            sell_take_profit=False, stp_atr=False, stp_value=2,
            sell_trailing_stop=False, sts_atr=False, sts_value=2,
            revert=False, fitness_function=False,
            data_index_date=False, data_with_indicators=False
    ):

        if not isinstance(data, DataClass):
            try:
                data_class = DataClass(data, index_date=data_index_date, with_indicators=data_with_indicators)
            except Exception as e:
                print('cold not convert data into DataClass, see DataClass documentation')
                raise e

        self.data_class = data_class

        if indicator_main_function and not isinstance(indicator_main_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(indicator_main_function)} in {indicator_main_function}')
            raise ValueError

        if buy_enter_function and not isinstance(buy_enter_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(buy_enter_function)}')
            raise ValueError

        if sell_enter_function and not isinstance(sell_enter_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(sell_enter_function)}')
            raise ValueError

        if sell_exit_function and not isinstance(sell_exit_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(sell_exit_function)}')
            raise ValueError

        if buy_exit_function and not isinstance(buy_exit_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(buy_exit_function)}')
            raise ValueError

        if fitness_function and not isinstance(fitness_function, types.FunctionType):
            print(f'indicator_main_function must be a function type, you insert a '
                  f'{type(fitness_function)}')
            raise ValueError

        self.inperiod = inperiod
        self.outperiod = outperiod
        self.indicator_main_function = indicator_main_function
        self.buy_enter_function = buy_enter_function
        self.sell_enter_function = sell_enter_function
        self.buy_exit_function = buy_exit_function
        self.sell_exit_function = sell_exit_function
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

        self.fitness_function = fitness_function
        if not fitness_function:
            self.fitness_function = result_return

    def run_walkfoward(self, x_list=[0], y_list=[0], z_list=[0], silent=False):
        df = self.data_class.dataframe.copy()

        max_indicator_global = max(max(x_list), max(y_list), max(z_list))

        dc_indices = {}

        in_start = len(df) - self.inperiod - self.outperiod
        out_start = len(df) - self.outperiod
        out_end = len(df)
        n = 0

        while in_start >= 0:
            dc_indices[n] = [in_start, out_start, out_end]
            n += 1
            in_start -= self.outperiod
            out_start -= self.outperiod
            out_end -= self.outperiod

        list_otimization = {}
        for key, value in dc_indices.items():
            i_final_otm = value[1]
            i_initial_otm = max(0, value[0] - max_indicator_global)
            if not silent:
                print(f'optimization {key}, initial: {i_initial_otm} final: {i_final_otm}, values={value}')

            parameter_fit = self.optimization(x_list, y_list, z_list, i_initial_otm, i_final_otm, silent=silent)

            list_otimization[key] = parameter_fit

        signal = 0
        i_start_df = dc_indices[len(list_otimization) - 1][1]
        for n in reversed(range(len(list_otimization))):

            x, y, z = list_otimization[n]

            if not silent:
                print(f'final_result {n}, x={x}, y={y}, z={z}')

            i_stop_calc = dc_indices[n][2]
            if i_start_df >= i_stop_calc:
                continue

            if not any(list_otimization[n]):
                df_wf = empty_backtest(self.data_class.dataframe, signal=signal)
            else:
                df_wf = self.backtesting(self.data_class.dataframe,
                                         x, y, z, dataframe=True, signal=signal, i_start=i_start_df)

            signal, i_end_df = wf_dataframe_signal_iend(df_wf, i_stop_calc)
            df_wf['n'], df_wf['x'], df_wf['y'], df_wf['z'] = n, x, y, z
            for i in range(len(df_wf)):
                if i < i_start_df:
                    df_wf.iloc[i, -4:] = 0

            if n == len(list_otimization) - 1:
                df_final = df_wf.iloc[:i_end_df + 1]
            else:
                df_final = pd.concat([df_final, df_wf.iloc[i_start_df: i_end_df + 1]])

            i_start_df = i_end_df + 1

        self.df_final = df_final

        return df_final

    def optimization(self, x_list, y_list, z_list, i_initial_otm, i_final_otm, silent=False):
        df = self.data_class.dataframe.copy()
        df = df.iloc[i_initial_otm:i_final_otm]

        i = 0
        parameters_fit = []
        list_fitness = []
        for x in x_list:
            for y in y_list:
                for z in z_list:
                    fitness = self.backtesting(df, x, y, z)
                    list_fitness.append(fitness)
                    if i == 0:
                        best_fit = fitness
                    i += 1
                    if fitness >= best_fit:
                        best_fit = max(best_fit, fitness)
                        parameters_fit = [x, y, z]
                    if not silent:
                        print(f'best_fit={best_fit:.3f}, fitness={fitness:.3f}, i={i}, x={x}, y={y}, z={z}')

        if not any(list_fitness):
            return [0, 0, 0]

        return parameters_fit

    def backtesting(self, df, x, y, z, dataframe=False, signal=0, i_start=0):
        back = Backtesting(df)

        if self.indicator_main_function:
            try:
                back.indicator(self.indicator_main_function, x, y, z)
            except TypeError:
                try:
                    back.indicator(self.indicator_main_function, x, y)
                except TypeError:
                    try:
                        back.indicator(self.indicator_main_function, x)
                    except TypeError:
                        back.indicator(self.indicator_main_function)

        if self.buy_enter_function:
            try:
                back.buy_enter(self.buy_enter_function, x, y, z)
            except TypeError:
                try:
                    back.buy_enter(self.buy_enter_function, x, y)
                except TypeError:
                    try:
                        back.buy_enter(self.buy_enter_function, x)
                    except TypeError:
                        back.buy_enter(self.buy_enter_function)

        if self.buy_exit_function:
            try:
                back.buy_exit(self.buy_exit_function, x, y, z)
            except TypeError:
                try:
                    back.buy_exit(self.buy_exit_function, x, y)
                except TypeError:
                    try:
                        back.buy_exit(self.buy_exit_function, x)
                    except TypeError:
                        back.buy_exit(self.buy_exit_function)

        if self.sell_enter_function:
            try:
                back.sell_enter(self.sell_enter_function, x, y, z)
            except TypeError:
                try:
                    back.sell_enter(self.sell_enter_function, x, y)
                except TypeError:
                    try:
                        back.sell_enter(self.sell_enter_function, x)
                    except TypeError:
                        back.sell_enter(self.sell_enter_function)

        if self.sell_exit_function:
            try:
                back.sell_exit(self.sell_exit_function, x, y, z)
            except TypeError:
                try:
                    back.sell_exit(self.sell_exit_function, x, y)
                except TypeError:
                    try:
                        back.sell_exit(self.sell_exit_function, x)
                    except TypeError:
                        back.sell_exit(self.sell_exit_function)

        back.backtesting(
            comission_enter=self.comission_enter, comission_exit=self.comission_exit,
            slippage_enter=self.slippage_enter, slippage_exit=self.slippage_exit,
            buy_stop_loss=self.buy_stop_loss, bsl_atr=self.bsl_atr, bsl_value=self.bsl_value,
            buy_take_profit=self.buy_take_profit, btp_atr=self.btp_atr, btp_value=self.btp_value,
            buy_trailing_stop=self.buy_trailing_stop, bts_atr=self.bts_atr, bts_value=self.bts_value,
            sell_stop_loss=self.sell_stop_loss, ssl_atr=self.ssl_atr, ssl_value=self.ssl_value,
            sell_take_profit=self.sell_take_profit, stp_atr=self.stp_atr, stp_value=self.stp_value,
            sell_trailing_stop=self.sell_trailing_stop, sts_atr=self.sts_atr, sts_value=self.sts_value,
            revert=self.revert, signal=signal, i_start=i_start,
        )

        back._dataframe_metrics(silent=True)

        if dataframe:
            return back.data_class.dataframe

        return self.fitness_function(back.df_metrics)

    def show_results(self):
        if self.df_final is None:
            print('df_final is None, run walkfoward test to create df_final')
            raise ValueError

        self.df_metrics = dataframe_metrics(self.df_final)

        self.df_metrics['return'] = np.where(
            self.df_metrics['short_long'] == 1,
            self.df_metrics['exit_price'] / self.df_metrics['enter_price'] - 1,
            self.df_metrics['enter_price'] / self.df_metrics['exit_price'] - 1
        )

        self.df_metrics['winrate'] = np.where(self.df_metrics['return'] > 0, 1, 0)

        self.trades_result = len(self.df_metrics)
        self.return_result = self.df_metrics['return'].sum()
        self.winrate_result = self.df_metrics['winrate'].mean()

        return {
            'trades': self.trades_result,
            'return': self.return_result,
            'winrate': self.winrate_result
        }
