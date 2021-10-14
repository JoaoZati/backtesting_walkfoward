import numpy as np


def moving_avarange_df(data_class, n, name='ma'):
    df = data_class.dataframe.copy()
    ma = np.array(df.close.rolling(n).mean())

    return {name: ma}