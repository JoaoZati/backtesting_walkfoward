from backtesting_numba.data_class import DataClass
import pandas as pd

data_sample = {
    'date': ['2021-04-01', '2021-04-02', '2021-04-03'],
    'open': [5.5, 6, 5.75],
    'high': [5.8, 7, 6.75],
    'low': [4.5, 5, 6.75],
    'close': [5.8, 5, 6.75]
}

data_class = DataClass(data_sample)

print(data_class.dataframe.columns)
columns = ['date', 'open', 'high', 'low', 'close']
for column in columns:
    if column in data_class.dataframe.columns:
        print('True')
    else:
        print('False')