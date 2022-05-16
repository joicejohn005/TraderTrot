from matplotlib import ticker
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

ticker = ['ZOMATO.NS','TCS.NS','WIpRO.NS'] # code to select stock
stock_info = yf.Ticker(ticker[0]).info
ticker = [i.upper() for i in ticker] # avoid if choosing from list of companies
ticker.sort()

index_ind = ['^NSEI','^BSESN'] 
for market in index_ind:
    if market in ticker:
        ticker.remove(market)
symbols = ticker + index_ind

#print(stock_info)
#print(symbols) #market index + stocks

yf_period = ['1d','5d','1m','3m','6m','ytd','1y','5y','max']
yf_interval = ['1m','5m','15m','30m','1h','4h','1d','1w','1mh']

#**********************************************************************************************#

#fin_info contain information that we need for analysing
fin_info = ["sector","industry","shortName","quoteType", "exchange", "totalAssets", "marketCap", "beta", "trailingPE", "volume", "averageVolume", "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "dividendRate", "phone"]
yf_info = pd.DataFrame(index = fin_info, columns=symbols)
# print(yf_info.head)

#**********************************************************************************************#

for i in symbols:
    l = []             # initialize
    x = yf.Ticker(i)   # get ticker info
    for j in fin_info:
        if 'date' in j.lower():
            d = pd.to_datetime(x.info[j])
            print(d)
            if d is not None:
                l.append(d.strftime("%Y-%m-%d"))  # format date
        else:
            try:      # some parameters error
                l.append(x.info[j])
            except:   # ignore error and continue
                l.append("")
    yf_info[i] = l
#print(yf_info) # print details of symbols in a table

#**********************************************************************************************#
#to see list of parameters 

# ticker_parameter = pd.DataFrame(stock_info).transpose()
# ticker_parameter = ticker_parameter.reset_index()
# ticker_parameter.rename(columns={'index':'PARAMETERS'}, inplace=True)
# ticker_parameter.sort_values(by=['PARAMETERS'],inplace=True)
# ticker_parameter.reset_index(drop=True, inplace=True)
# print(ticker_parameter)

#**********************************************************************************************#
print('SYMBOLS:\n{}\n'.format(symbols))
print('PERIOD:\t\t{}'.format(yf_period))
print('INTERVAL:\t{}'.format(yf_interval))

yf_returns = yf.download(
        tickers = symbols,       # tickers list or string as well
        period = yf_period,      # optional, default is '1mo'
        interval = yf_interval,  # fetch data by intervaal
        group_by = 'ticker',     # group by ticker
        auto_adjust = True,      # adjust all OHLC (open-high-low-close)
        prepost = True,          # download market hours data
        threads = True,          # threads for mass downloading
        proxy = None)            # proxy
yf_returns = yf_returns.iloc[:, yf_returns.columns.get_level_values(1)=='Close']
# yf_returns = yf_returns.iloc[:, yf_returns.columns.get_level_values(1)=='Close']
# yf_returns.columns = yf_returns.columns.droplevel(1)  # multi-index
# yf_returns.tail(10)
# print('shape: ', yf_returns.shape)

#**********************************************************************************************#

#yf_dividend = yf.Ticker(ticker[1]).dividends
# print(dividends)

# #performance
# annual_info = 1
# print(annual_info)