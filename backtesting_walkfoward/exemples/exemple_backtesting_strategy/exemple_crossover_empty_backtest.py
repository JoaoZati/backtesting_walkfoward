import os
import pandas as pd
from backtesting_walkfoward.backtesting import Backtesting


if __name__ == '__main__':
    try:
        os.chdir('backtesting_walkfoward/exemples/exemple_backtesting_strategy')
        print('ok')
    except Exception:
        pass

    path = '../../sample_data/AAPL.csv'
    df_aapl = pd.read_csv(path)

    backtesting = Backtesting(df_aapl)

    backtesting.backtesting(timeit=True, signal=-1)
