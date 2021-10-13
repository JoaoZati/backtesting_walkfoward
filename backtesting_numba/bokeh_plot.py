from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import CrosshairTool, HoverTool, ResetTool, PanTool, WheelZoomTool, BoxZoomTool, SaveTool
from bokeh.layouts import gridplot

import pandas as pd
import numpy as np


def bokeh_df(DF, title):
    df = DF.copy()
    bool_volume = False

    seqs = np.arange(df.shape[0])
    df["seq"] = pd.Series(seqs)
    df['mid'] = df.apply(lambda x: (x['open'] + x['close']) / 2, axis=1)
    df['height'] = df.apply(lambda x: abs(x['close'] - x['open'] if x['close'] != x['open'] else 0.001), axis=1)

    try:
        df['volume'] = np.where(df['volume'] == 0, 1, df['volume'])
        df['mid vol'] = df.apply(lambda x: x['volume'] / 2, axis=1)
        bool_volume = True
    except Exception:
        pass

    df['high'] = np.where(df['high'] == df['close'], df['high'] + 0.001, df['high'])
    df['low'] = np.where(df['low'] == df['close'], df['low'] - 0.001, df['low'])

    # Manipulando Sorceinc e Tools #
    inc = df["close"] >= df["open"]
    dec = df["open"] > df["close"]
    w = 0.8

    # use ColumnDataSource to pass in data for tooltips
    sourceInc = ColumnDataSource(ColumnDataSource.from_df(df.loc[inc]))
    sourceDec = ColumnDataSource(ColumnDataSource.from_df(df.loc[dec]))

    # the values for the tooltip come from ColumnDataSource
    hover = HoverTool(
        tooltips=[
            ("date", "@date"),
            ("seq", "@seq"),
            ("open", "@open"),
            ("high", "@high"),
            ("low", "@low"),
            ("close", "@close"),
        ]
    )

    TOOLS = [CrosshairTool(), PanTool(), WheelZoomTool(), ResetTool(), BoxZoomTool(), SaveTool(), hover]

    # Figure Bokeh #

    p = figure(plot_width=1500, plot_height=400, tools=TOOLS, title=title, x_axis_location="above")
    p.xaxis.major_label_orientation = 0
    p.grid.grid_line_alpha = 0.3

    # this is the up/down tails
    p.segment(df.seq[inc], df.high[inc], df.seq[inc], df.low[inc], color="black")
    p.segment(df.seq[dec], df.high[dec], df.seq[dec], df.low[dec], color="black")
    # this is the candle body for the up/down dates
    p.rect(x='seq', y='mid', width=w, height='height', fill_color="black", line_color="black", source=sourceDec)
    p.rect(x='seq', y='mid', width=w, height='height', fill_color="white", line_color="black", source=sourceInc)

    # Figura volume #
    pv = figure(plot_width=1500, plot_height=200, tools=TOOLS, x_range=p.x_range)
    pv.xaxis.major_label_orientation = 0
    pv.grid.grid_line_alpha = 0.3

    if bool_volume:
        pv.rect(x='seq', y='mid vol', width=w, height='volume', fill_color="blue", line_color="blue", source=sourceDec)
        pv.rect(x='seq', y='mid vol', width=w, height='volume', fill_color="white", line_color="blue", source=sourceInc)

    return p, pv


def bokeh_ohlcv_step(ohlcv, p, indicator, color):
    # Need 'Stop_Level
    df = ohlcv.copy()
    df.reset_index(inplace=True)
    seqs = np.arange(df.shape[0])
    df["seq"] = pd.Series(seqs)

    p.step(df["seq"], df[indicator], line_width=1, color=color, mode="center")

    return p


def bokeh_ohlcv_line(ohlcv, p, indicator, color):
    # Need 'Stop_Level
    df = ohlcv.copy()
    df.reset_index(inplace=True)
    seqs = np.arange(df.shape[0])
    df["seq"] = pd.Series(seqs)

    p.line(df["seq"], df[indicator], line_width=1, color=color)

    return p


def bokeh_ohlcv_circle(ohlcv, p, indicator, color):
    # Need 'Stop_Level
    df = ohlcv.copy()
    df.reset_index(inplace=True)
    seqs = np.arange(df.shape[0])
    df["seq"] = pd.Series(seqs)

    p.circle(df["seq"], df[indicator], size=10, color=color)

    return p


def bokeh_gridplot(p, pv):
    show(gridplot([[p], [pv]]))
