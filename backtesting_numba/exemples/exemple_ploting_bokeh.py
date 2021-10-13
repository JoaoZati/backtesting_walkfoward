import os
import pandas as pd

from backtesting_numba import bokeh_plot as bk

try:
    os.chdir('backtesting_numba/exemples')
except Exception:
    pass

path = '../sample_data/AAPL.csv'
df_aapl = pd.read_csv(path)

p, pv = bk.bokeh_df(df_aapl, 'Apple')
bk.bokeh_gridplot(p, pv)
