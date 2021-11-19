# backtesting_walkfoward
This is a python library to make backtesting and walkfoward testing with financial data.

## Technologies
Python 3

[![Build Status](https://app.travis-ci.com/JoaoZati/backtesting_walkfoward.svg?branch=main)](https://app.travis-ci.com/JoaoZati/backtesting_walkfoward)
[![Updates](https://pyup.io/repos/github/JoaoZati/backtesting-numba/shield.svg)](https://pyup.io/repos/github/JoaoZati/backtesting-numba/)
[![Python 3](https://pyup.io/repos/github/JoaoZati/backtesting-numba/python-3-shield.svg)](https://pyup.io/repos/github/JoaoZati/backtesting-numba/)

## Setup
```
pip install backtesting-walkfoward
```
or
```
git clone https://github.com/JoaoZati/backtesting_walkfoward.git
```

## Exemple how to use
### Buildin a backtesting and a walkfoward testing of a crossover strategy

### Backtesting:

#### 1. Import packages 
```
from backtesting_walkfoward.backtesting import Backtesting
import numpy as np
import pandas as pd
```

#### 2. Download of financial data (from csv, json etc..) and transform to pandas.
#### obs:
####  your data must contain ['date', 'open', 'high', 'low', 'close'] as column.
####  you can place indicators in dataframe, but it cant be optimized in walkfoward and you should pass with_indicators=True. It's great for fundamental data and web scraped data.
#### if you are passing a dataframe you can pass date as index with index_date=True.

```
data_yf = DownloadData('MSFT')
df_msft = data_yf.dataframe.copy()
```

#### 4. You can start you backtesting;
```
backtesting = Backtesting(df_msft)
```

#### You can plot the ohcl data in bokeh to see how the download data;

```
backtesting.data_class.plot_bokeh_ohlc()
```

#### 5. Create one indicators functions with data_class as first parameter (if your strategy use indicators).

```
def moving_avarange(data_class, x, y):
    df = data_class.dataframe.copy()
    ma_fast = np.array(df.close.rolling(x).mean())
    ma_slow = np.array(df.close.rolling(y).mean())

    return {'ma_fast': ma_fast, 'ma_slow': ma_slow}
```

#### pass it backtesting object with x and y volue (pass values to indicators args, can make in indicator function how many args you want):

```
backtesting.indicator(moving_avarange, 12, 200)
```

#### 6. Create your logic entry and exits. Note you can create: Buy Enter, Buy Close, Sell Enter, Sell Close. For stop loss or trailing stop you dont need create a function. Its implemented in backtesting (see more later).
```
def buy_enter_ma(data_class):
    mf = data_class.indicators['ma_fast']
    ms = data_class.indicators['ma_slow']
    op = data_class.open
    be = np.zeros(len(mf))

    for i in range(len(be)):
        if i < 2 or not mf[i] or not ms[i]:
            continue
        if mf[i - 2] <= ms[i - 2] and mf[i - 1] > ms[i - 1]:
            be[i] = op[i]

    return be
```

```
def sell_enter_ma(data_class):
    mf = data_class.indicators['ma_fast']
    ms = data_class.indicators['ma_slow']
    op = data_class.open
    se = np.zeros(len(mf))

    for i in range(len(se)):
        if i < 2 or not mf[i] or not ms[i]:
            continue
        if mf[i - 2] >= ms[i - 2] and mf[i - 1] < ms[i - 1]:
            se[i] = op[i]

    return se
```

#### note: the only two rules are: first it need data_class as first parameter and should return one numpy array with 1 column.

#### pass to backtesting

```
backtesting.buy_enter(buy_enter_ma)
backtesting.sell_enter(sell_enter_ma)
```

#### 7. Now with data, indicator and logic rules all setup done you can run your backtestings;

```
backtesting.backtesting(revert=True)
```

#### note 1: I run revert=True, it makes the backtesting close order and open a new order in inverse direction. Ex: In a candle the simulation are long, but a sell signal was made. It closes the long position and sell after that.

#### note 2: You can run sell_stop_loss=True, buy_stop_loss=True to set stop losses and set values with ssl_value=<value> and bsl_value=<value> respectively. 

#### there are some other functions like set commissions and slipage fee. For more details see exemples.

#### 8. You can see the results and the backtesting plot to see if the logic was implemented correctly:

#### See metrics, it returns a dictionary with number of trades, total return and winrate:

```
metrics_results = backtesting.results()
```

#### For plot return just run:

```
backtesting.data_class.plot_bokeh_indicators(
    line_indicators={'ma_fast': 'blue', 'ma_slow': 'yellow'},
    circle_indicators={'buy_enter_price': 'green', 'sell_enter_price': 'red'}
)
```

#### You can control what are the indicators you want to see with line_indicators and circle_indicators.

### Walkfoard Testing:

#### 1. How we already have the data, indicator function and logic functions. To setup walkfowad you just need to:

```
walkfoward = WalkFoward(
    df_msft, 500, 1000,
    indicator_main_function=moving_avarange,
    buy_enter_function=buy_enter_ma, sell_enter_function=sell_enter_ma,
    revert=True
)
```

#### 500 is inperiod numbers of candles and 1000 is outperiod numbers of candles.

#### 2. Run walkfoward testing:

```
result_walkfoward = walkfoward.run_walkfoward(x_list=[12, 20, 30], y_list=[100, 200, 300], z_list=[0])
```

#### 3. For the metrics results, with numbers of trades, return and winrate just run:

```
metrics_walkfoward = walkfoward.show_results()
```

#### 4. For plot the results. Just create a DataClass with result_walkfoward with indicators and plot it:

```
data_wf.plot_bokeh_indicators(
    line_indicators={'ma_fast': 'blue', 'ma_slow': 'yellow'},
    circle_indicators={'buy_enter_price': 'green', 'sell_enter_price': 'red'},
    title='Walkfowad Crossover AAPL'
)
```