from backtesting_walkfoward.backtesting import Backtesting
import pandas as pd
import os
from backtesting_walkfoward.exemples.exemple_numba.exemple_numba import moving_avarange_njit

try:
    os.chdir('backtesting_walkfoward/exemples/exemple_backtesting_indicator')
except Exception:
    pass

path = '../../sample_data/AAPL.csv'
df_aapl = pd.read_csv(path)

backtesting = Backtesting(df_aapl)
backtesting.indicator(moving_avarange_njit, 20, 120)

print(backtesting.data_class.dataframe)
