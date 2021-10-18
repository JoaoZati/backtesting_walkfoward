import numpy as np


def moving_avarange_df(data_class, n, name='ma'):
    df = data_class.dataframe.copy()
    ma = np.array(df.close.rolling(n).mean())

    return {name: ma}


def atr(data_class, n, erm=False):
    "function to calculate True Range and Average True Range"
    df = data_class.dataframe.copy()

    df['H-L'] = abs(df['high'] - df['low'])
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    if erm:
        df['ATR'] = df['TR'].ewm(span=n, adjust=False, min_periods=n).mean()
    else:
        df['ATR'] = df['TR'].rolling(n).mean()

    return {'atr': df['ATR']}
