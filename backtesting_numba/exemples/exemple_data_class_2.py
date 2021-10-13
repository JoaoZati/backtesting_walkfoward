from backtesting_numba.data_class import DataClass
import pandas as pd

path = '../sample_data/AAPL.csv'
df_aapl = pd.read_csv(path)

dataclass_aapl = DataClass(df_aapl)
