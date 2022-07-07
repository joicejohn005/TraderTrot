from datetime import datetime
from distutils.log import info
from matplotlib import ticker
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

def analy(ticker):
    yf_period   = "5y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
    yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    yf_returns = yf.download(
            tickers = ticker,       # tickers list or string as well
            period = yf_period,      # optional, default is '1mo'
            interval = yf_interval,  # fetch data by intervaal
            group_by = 'ticker',     # group by ticker
            auto_adjust = True,      # adjust all OHLC (open-high-low-close)
            prepost = True,          # download market hours data
            threads = True,          # threads for mass downloading
            proxy = None)            # proxy

    yf_returns = yf_returns.iloc[:, yf_returns.columns.get_level_values(0)=='Close']

    yf_divdend = pd.DataFrame()   # initialize dataframe
    for i in ticker:
        x = pd.DataFrame(yf.Ticker(i).dividends)
        yf_divdend = pd.concat([yf_divdend,x], axis=1) 
    #  match dates in yf_returns (first return data to now)
    #  print out dividends

    yf_divdend = yf_divdend[yf_divdend.index >= yf_returns.index[0]]
    return(yf_divdend)
 