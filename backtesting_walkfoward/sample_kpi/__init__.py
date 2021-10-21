def mean_return(backtesting):
    if backtesting.df_metrics is None:
        backtesting.results(silent=True)

    df = backtesting.df_metrics.copy()

    return df['return'].mean()
