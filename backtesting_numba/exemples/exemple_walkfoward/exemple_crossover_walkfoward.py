import os
import pandas as pd
from backtesting_numba.walkfoward import WalkFoward
from backtesting_numba.data_class import DataClass
import numpy as np


def walkfoward_moving_avarange(data_class, x, y):
    df = data_class.dataframe.copy()
    ma_fast = np.array(df.close.rolling(x).mean())
    ma_slow = np.array(df.close.rolling(y).mean())

    return {'ma_fast': ma_fast, 'ma_slow': ma_slow}


def walkfoward_buy_enter_ma(data_class):
    mf = data_class.indicators['ma_fast']
    ms = data_class.indicators['ma_slow']
    op = data_class.open
    be = np.zeros(len(mf))

    for i in range(len(be)):
        if i < 2 or not mf[i] or not ms[i]:
            continue
        if mf[i - 2] <= ms[i - 2] and mf[i - 1] > ms[i - 1]:
            be[i] = op[i]

    return be


def walkfoward_sell_enter_ma(data_class):
    mf = data_class.indicators['ma_fast']
    ms = data_class.indicators['ma_slow']
    op = data_class.open
    se = np.zeros(len(mf))

    for i in range(len(se)):
        if i < 2 or not mf[i] or not ms[i]:
            continue
        if mf[i - 2] >= ms[i - 2] and mf[i - 1] < ms[i - 1]:
            se[i] = op[i]

    return se


if __name__ == '__main__':
    try:
        os.chdir('backtesting_numba/exemples/exemple_walkfoward')
        print('ok')
    except Exception:
        pass

    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)

    walkfoward = WalkFoward(
        df_aapl, 500, 1000,
        indicator_main_function=walkfoward_moving_avarange,
        buy_enter_function=walkfoward_buy_enter_ma, sell_enter_function=walkfoward_sell_enter_ma,
        revert=True
    )

    result_walkfoward = walkfoward.run_walkfoward(x_list=[12, 20, 30], y_list=[100, 200, 300], z_list=[0])

    metrics_walkfoward = walkfoward.show_results()

    data_wf = DataClass(result_walkfoward, with_indicators=True)
    data_wf.plot_bokeh_indicators(
        line_indicators={'ma_fast': 'blue', 'ma_slow': 'yellow'},
        circle_indicators={'buy_enter_price': 'green', 'sell_enter_price': 'red'},
        title='Walkfowad Crossover AAPL'
    )
