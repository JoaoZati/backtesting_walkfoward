from backtesting_numba.data_class import DataClass
import os
import pandas as pd

try:
    os.chdir('backtesting_numba/exemples')
except Exception:
    pass

path = '../sample_data/AAPL.csv'
df_aapl = pd.read_csv(path)
sr_volume = df_aapl.volume

dataclass_aapl = DataClass(df_aapl)
dataclass_aapl.add_update_indicator('volume', sr_volume)

print(dataclass_aapl.dataframe)
