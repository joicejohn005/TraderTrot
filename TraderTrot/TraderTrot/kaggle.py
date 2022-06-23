from matplotlib import ticker
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf

ticker = ['ZOMATO.NS','TCS.NS','WIPRO.NS'] # code to select stock
stock_info = yf.Ticker(ticker[0]).info
ticker = [i.upper() for i in ticker] # avoid if choosing from list of companies
ticker.sort()

index_ind = ['^NSEI','^BSESN'] 
for market in index_ind:
    if market in ticker:
        ticker.remove(market)
symbols = ticker + index_ind

#print(symbols) #market index + stocks

# yf_period = ['1d','5d','1m','3m','6m','1y','5y']
# yf_interval = ['1m','5m','15m','30m','1h','4h','1d','1w','1mh']

yf_period   = "20y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo


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
print(yf_info) # print details of symbols in a table

#**********************************************************************************************#
#to see list of parameters 

# ticker_parameter = pd.DataFrame(stock_info).transpose()
# ticker_parameter = ticker_parameter.reset_index()
# ticker_parameter.rename(columns={'index':'PARAMETERS'}, inplace=True)
# ticker_parameter.sort_values(by=['PARAMETERS'],inplace=True)
# ticker_parameter.reset_index(drop=True, inplace=True)
# print(ticker_parameter)

#**********************************************************************************************#
# print('SYMBOLS:\n{}\n'.format(symbols))
# print('PERIOD:\t\t{}'.format(yf_period))
# print('INTERVAL:\t{}'.format(yf_interval))

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
yf_returns.columns = yf_returns.columns.droplevel(1)  # multi-index
print(yf_returns.tail(10))
print('shape: ', yf_returns.shape)

#**********************************************************************************************#
#percentage change

yf_returns = round(yf_returns.pct_change()*100, 2)
print(yf_returns.tail(10))

#**********************************************************************************************#
#Dividend Percentages
yf_divdend = pd.DataFrame()   # initialize dataframe

for i in ticker:
    if i != index_ind:
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

#**********************************************************************************************#
#Calculate Percentage Returns
#yf_returns = yf_returns + yf_divdend    // - Equation | not code

yf_returns = yf_returns.add(yf_divdend, fill_value = 0)
#print(yf_returns.tail(5))
#**********************************************************************************************#

#Performance Analysis:
perf_dy = yf_returns
perf_dy['YEAR']  = perf_dy.index.strftime("%Y")     # YEAR
perf_dy['MONTH'] = perf_dy.index.strftime("%Y-%m")  # YEAR-MONTH
perf_dy['WEEK']  = perf_dy.index.strftime("%Y-%U")  # YEAR-WEEK

#  create time dataframes using GROUPBY
perf_yr = perf_dy.groupby('YEAR').sum()
perf_mh = perf_dy.groupby('MONTH').sum()
perf_wk = perf_dy.groupby('WEEK').sum()


#  print index and column names

# print("\nperf_dy:\n", perf_dy.index.name, perf_dy.columns.values)
# print("\nperf_yr:\n", perf_yr.index.name, perf_yr.columns.values)
# print("\nperf_mh:\n", perf_mh.index.name, perf_mh.columns.values)
# print("\nperf_wk:\n", perf_wk.index.name, perf_wk.columns.values)

#**********************************************************************************************#

#  create function to plot market and indexes
def plotPerformance(arg):
    df = arg
    
    plt.figure(figsize=(10,8))

    #  subplot #1
    plt.subplot(221)
    df[index_ind].boxplot()
    plt.title('market indexes')
    plt.ylabel('percent change')
    plt.xticks(rotation = 90)
    plt.grid(False)

    #  subplot #2
    plt.subplot(222)
    plt.plot(df[index_ind])
    plt.title('market indexes')
    plt.legend(df[index_ind], loc="upper left", bbox_to_anchor=(1,1))
    plt.xticks(rotation = 90)
    
    plt.show()  # plot subplots
    
    #  plot #3
    plt.figure(figsize=(10,6))
    df[ticker].boxplot()
    plt.title('SYMBOLS', fontsize = 14)
    plt.ylabel('percent change', fontsize = 14)
    plt.xticks(rotation = 90)
    plt.grid(False)
    plt.show()
    
    #  plot #4
    plt.figure(figsize=(10,6))
    plt.plot(df[ticker])
    plt.title('SYMBOLS', fontsize = 14)
    plt.ylabel('percent change', fontsize = 14)
    plt.legend(df[ticker], loc="upper left", bbox_to_anchor=(1,1))
    plt.xticks(rotation = 90)
    plt.show()
    

    #  print returns
    print('\nRETURNS FROM {} TO {}:'.format(df.index[0], df.index[-1]))
    for i in index_ind + ticker:
        print('{:>10}{:>10.2f}%'.format(i,df[i].sum()))

    return

print('function plotPerformance created')

#**********************************************************************************************#
#Plot and analyze the yearly performance for the past 10 years (past decade).
plotPerformance(perf_yr.tail(10))  # past 10 years

#**********************************************************************************************#
#plotPerformance(perf_mh.tail(24))  # past 24 months
plotPerformance(perf_mh.tail(24))  # past 24 months
#**********************************************************************************************#
#Plot and analyze the yearly performance for the past 26 weeks (6 months).
plotPerformance(perf_wk.tail(26))  # past 26 weeks
#**********************************************************************************************#
#Plot and analyze the yearly performance for the past 31 days (1 month).
plotPerformance(perf_dy.tail(31))  # past 31 days

#yf_dividend = yf.Ticker(ticker[1]).dividends
# print(dividends)

# #performance
# annual_info = 1
# print(annual_info)