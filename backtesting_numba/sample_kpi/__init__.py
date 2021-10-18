import numpy as np
import pandas as pd


def buy_enter_exit_df(df_input):
    df = df_input.copy()

    df_buy_enter_price = df[['date', 'buy_enter_price']].replace(0, np.nan)
    df_buy_enter_price.dropna(inplace=True)
    df_buy_enter_price['short_long'] = 1
    df_buy_exit_price = df[['date', 'buy_exit_price']].replace(0, np.nan)
    df_buy_exit_price.dropna(inplace=True)

    if len(df_buy_enter_price) != len(df_buy_exit_price):
        print(f'Size of df_buy_enter_price is {len(df_buy_enter_price)} and Size of '
              f'df_buy_exit_price is {len(df_buy_exit_price)}!')
        if len(df_buy_enter_price) == len(df_buy_exit_price) + 1:
            print('deleting last db_buy_enter_price')
            df_buy_enter_price = df_buy_enter_price.iloc[:-1]

    dict_buy = {
        'candle_enter': np.array(df_buy_enter_price.index),
        'candle_exit': np.array(df_buy_exit_price.index),
        'date_enter': np.array(df_buy_enter_price['date']),
        'date_exit': np.array(df_buy_exit_price['date']),
        'short_long': np.array(df_buy_enter_price['short_long']),
        'enter_price': np.array(df_buy_enter_price['buy_enter_price']),
        'exit_price': np.array(df_buy_exit_price['buy_exit_price']),
    }

    df_buy = pd.DataFrame(dict_buy)

    return df_buy


def sell_enter_exit_df(df_input):
    df = df_input.copy()

    df_sell_enter_price = df[['date', 'sell_enter_price']].replace(0, np.nan)
    df_sell_enter_price.dropna(inplace=True)
    df_sell_enter_price['short_long'] = -1
    df_sell_exit_price = df[['date', 'sell_exit_price']].replace(0, np.nan)
    df_sell_exit_price.dropna(inplace=True)

    if len(df_sell_enter_price) != len(df_sell_exit_price):
        print(f'Size of df_sell_enter_price is {len(df_sell_enter_price)} and Size of '
              f'df_sell_exit_price is {len(df_sell_exit_price)}!')
        if len(df_sell_enter_price) == len(df_sell_exit_price) + 1:
            print('deleting last db_sell_enter_price')
            df_sell_enter_price = df_sell_enter_price.iloc[:-1]

    dict_sell = {
        'candle_enter': np.array(df_sell_enter_price.index),
        'candle_exit': np.array(df_sell_exit_price.index),
        'date_enter': np.array(df_sell_enter_price['date']),
        'date_exit': np.array(df_sell_exit_price['date']),
        'short_long': np.array(df_sell_enter_price['short_long']),
        'enter_price': np.array(df_sell_enter_price['sell_enter_price']),
        'exit_price': np.array(df_sell_exit_price['sell_exit_price']),
    }

    df_sell = pd.DataFrame(dict_sell)

    return df_sell


def df_metrics(data_class):
    df_buy = buy_enter_exit_df(data_class.dataframe)
    df_sell = sell_enter_exit_df(data_class.dataframe)

    df_metrics = pd.concat([df_buy, df_sell])
    df_metrics.sort_values(by=['date_enter'], inplace=True)

    return df_buy, df_sell, df_metrics
