from matplotlib import ticker
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

ticker = ['TCS.NS'] # code to select stock
stock_info = yf.Ticker(ticker[0]).info #print(stock_info) to get information of stock

# index_ind = ['^NSEI','^BSESN'] # code to select index
# for market in index_ind:
#     if market in ticker:
#         ticker.remove(market)
# symbols = ticker + index_ind #to club all ticker + index into a list

#user input
yf_period   = "20y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

#fin_info contain information that we need for analysing
fin_info = ["sector","industry","shortName","quoteType", "exchange", "totalAssets", "marketCap", "beta", "trailingPE", "volume", "averageVolume", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "dividendRate", "phone"]
yf_info = pd.DataFrame(index = fin_info, columns=ticker)
for i in ticker:
    l = []             # initialize
    x = yf.Ticker(i)   # get ticker info
    for j in fin_info:
        if 'date' in j.lower():
            d = pd.to_datetime(x.info[j])
            if d is not None:
                l.append(d.strftime("%Y-%m-%d"))  # format date
        else:
            try:      # some parameters error
                l.append(x.info[j])
            except:   # ignore error and continue
                l.append("")
    yf_info[i] = l
#print(yf_info)
yf_returns = yf.download(
        tickers = ticker,       # tickers list or string as well
        period = yf_period,      # optional, default is '1mo'
        interval = yf_interval,  # fetch data by intervaal
        group_by = 'ticker',     # group by ticker
        auto_adjust = True,      # adjust all OHLC (open-high-low-close)
        prepost = True,          # download market hours data
        threads = True,          # threads for mass downloading
        proxy = None)            # proxy

print(yf_returns.tail(1)) # OHLC of last day | put number of days in tail.

yf_divdend = pd.DataFrame()   # initialize dataframe

for i in ticker:
    
    x = pd.DataFrame(yf.Ticker(i).dividends)
    x = x.rename(columns={"Dividends":i})
    yf_divdend = pd.concat([yf_divdend,x], axis=1)
    if len(x) > 0:
        print('{:>8}\t- dividends'.format(i))
    else:
        print('{:>8}\t- no dividends'.format(i))             

#  match dates in yf_returns (first return data to now)
yf_divdend = yf_divdend[yf_divdend.index >= yf_returns.index[0]]


#  print out dividends
print("\n",yf_divdend.tail(10))