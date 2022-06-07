from distutils.log import info
from matplotlib import ticker
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

ticker = ['TCS.NS'] # code to select stock
stock_info = yf.Ticker(ticker[0]).info #print(stock_info) to get information of stock

stock_info['dayLow']
stock_info['dayHigh']

x=stock_info['currentPrice']

stock_info['fiftyTwoWeekHigh']
stock_info['fiftyTwoWeekLow']

y=stock_info['previousClose']
d=x-y
p=(d/y)*100
print(stock_info)
#user input

yf_period   = "10y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

#fin_info contain information that we need for analysing

# fin_info = ["sector","industry","shortName","quoteType", "exchange", "totalAssets", "marketCap", "beta", "trailingPE", "volume", "averageVolume", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "dividendRate", "phone"]
# yf_info = pd.DataFrame(index = fin_info, columns=ticker)

# print close prices
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
print(yf_returns.tail(5))


#day % change
yf_returns = round(yf_returns.pct_change()*100, 2)
print(yf_returns.tail(5))


yf_divdend = pd.DataFrame()   # initialize dataframe
for i in ticker:
    x = pd.DataFrame(yf.Ticker(i).dividends)
    # x = x.rename(columns={"Dividends":i}) #to rename column name
    yf_divdend = pd.concat([yf_divdend,x], axis=1) 
#  match dates in yf_returns (first return data to now)
#  print out dividends
yf_divdend = yf_divdend[yf_divdend.index >= yf_returns.index[0]]
print("\n",yf_divdend.tail(13)) # rs give by company per share with corresponding dates


# yf_returns = yf_returns.add(yf_divdend, fill_value = 0)
# print(yf_returns.tail(5))

#  create YEAR, MONTH, WEEK columns in perf_dy


# perf_dy = yf_returns
# perf_dy['YEAR']  = perf_dy.index.strftime("%Y")     # YEAR
# perf_dy['MONTH'] = perf_dy.index.strftime("%Y-%m")  # YEAR-MONTH
# perf_dy['WEEK']  = perf_dy.index.strftime("%Y-%U")  # YEAR-WEEK


# #  create time dataframes using GROUPBY
# perf_yr = perf_dy.groupby('YEAR').sum()
# perf_mh = perf_dy.groupby('MONTH').sum()
# perf_wk = perf_dy.groupby('WEEK').sum()


# #  print index and column names
# print("\nperf_dy:\n", perf_dy.index.name, perf_dy.columns.values)
# print("\nperf_yr:\n", perf_yr.index.name, perf_yr.columns.values)
# print("\nperf_mh:\n", perf_mh.index.name, perf_mh.columns.values)
# print("\nperf_wk:\n", perf_wk.index.name, perf_wk.columns.values)
