import yfinance as yf
from equityanalyst import stock_price_predict
from equityanalyst import get_stock_data
from equityanalyst import plot_stock_data

y = stock_price_predict('ZOMATO.NS')
print(y)
