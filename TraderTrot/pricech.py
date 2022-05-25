#from ast import Index, pattern
from matplotlib.pyplot import text
import pandas as pd
import datetime
import yfinance as yf
from requests import request
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts


def real_time_price(symbol):

    #link of website to be scrapped
    url = 'https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol + '&.tsrc=fin-srch'

    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')

        #to get price & change %

        texts = web_content_div(web_content, 'D(ib) Va(m) Maw(65%) Ov(h)')
        if texts != []:
            price, change = texts[0], texts[1]
        else:
            price, change =[], []


        # #to get Volume - method 1(scrapping)
        # texts = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')
        # if texts != []:
        #     for count, vol in enumerate(texts):
        #         if vol == 'Volume':
        #             volume = texts[count+1]
        # else:
        #     volume = []

        # #yahoo technical analysis that states,stock is bearish/bullish or neutral
        # pattern = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb)')
        # try:
        #     latest_pattern = pattern[0]
        # except IndexError:
        #     latest_pattern = []

        # texts = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)')
        # if texts != []:
        #     for count, target in enumerate(texts):
        #         if target =='1y Target Est':
        #             one_year_target = texts[count+1]
        # else:
        #     one_year_target = []

    except ConnectionError:
        price,change, volume, latest_pattern, one_year_target =[], [],[], [], []
    return price, change
    #, volume, latest_pattern, one_year_target

# def stocklist():
#     df = pd.read_csv('app/equity.csv')
#     nselist = df['SYMBOL'].tolist()  #coloumn name :SYMBOL
#     return nselist

#s=input("ENTER THE STOCK ")
Stock = ['ZOMATO.NS']
#print(yf.Ticker('ZOMATO.NS').info['open'])
print(real_time_price('ZOMATO.NS'))