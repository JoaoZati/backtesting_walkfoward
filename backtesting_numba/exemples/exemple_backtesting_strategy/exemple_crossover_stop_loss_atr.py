import os
import pandas as pd
from backtesting_numba.backtesting import Backtesting
import backtesting_numba.sample_indicators as bni
from backtesting_numba.sample_rules import buy_enter, sell_enter

if __name__ == '__main__':
    try:
        os.chdir('backtesting_numba/exemples/exemple_backtesting_strategy')
        print('ok')
    except Exception:
        pass

    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)

    backtesting = Backtesting(df_aapl)

    backtesting.indicator(bni.moving_avarange_df, 20, 'ma_20')
    backtesting.indicator(bni.moving_avarange_df, 200, 'ma_200')
    backtesting.indicator(bni.atr, 2)

    backtesting.buy_enter(buy_enter.buy_enter_crossover, 'ma_20', 'ma_200')
    backtesting.sell_enter(sell_enter.sell_enter_crossover, 'ma_20', 'ma_200')

    backtesting.backtesting(buy_stop_loss=True, bsl_atr=True, sell_stop_loss=True, ssl_atr=True,
                            revert=True, timeit=True)

    backtesting.data_class.plot_bokeh_indicators(
        line_indicators={'ma_20': 'blue', 'ma_200': 'yellow'},
        circle_indicators={
            'buy_exit_price': 'orange', 'sell_exit_price': 'orange',
            'buy_enter_price': 'green', 'sell_enter_price': 'red',
        },
        step_indicators={
            'stop_loss_level': 'red',
        }
    )
