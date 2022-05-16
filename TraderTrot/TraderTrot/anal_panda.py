from cProfile import label
import datetime
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
start = datetime.datetime(2022, 4, 5)
end = datetime.datetime.now()
stock = web.DataReader('ZOMATO.NS','yahoo',start,end)
stock2 = web.DataReader('COFFEEDAY.NS','yahoo',start,end)
stock3 = web.DataReader('IDEA.NS','yahoo',start,end)
stock['Total Traded'] = stock3['Open'] * stock['Volume']

# stock.to_csv('Zomato.csv')
print(stock)
stock['Open'].plot(label="Open Price",figsize=(13,6))
stock['Close'].plot(label="Close Price")
stock['High'].plot(label="High Price")
stock['Low'].plot(label="Low Price")

stock['Open'].plot(label="Zomato")
stock2['Open'].plot(label="Coffeday")
stock3['Open'].plot(label="Idea")

plt.legend()
plt.title('Zomato Stock price')
plt.xlabel('Date')
plt.xlabel('Stock Price')
plt.show()