from bs4 import BeautifulSoup

import pandas as pd
import datetime
from requests import request
import requests
from requests.exceptions import ConnectionError
import urllib.request

#to store scrapped data
def scrap_procon(ticker):
    # url = 'https://www.screener.in/company/' +ticker+ '/consolidated/'
    # webpage = requests.get(url) #Request to webpage
    # soup = BeautifulSoup(webpage.text,'html.parser') #parse text frm website

    # prosText = soup.find_all('div',attrs={'class':'pros'})
    # for i in prosText:
    #     pros = i.text.split('. ')
   
    # prolist=[]
    
    # for i in pros: 
    #     i = i.replace("Pros","")
    #     prolist.append(i)
      
    # for i in prolist:
    #     print("k")
    #     print(i)
    
    url2 = 'https://www.nseindia.com/get-quotes/equity?symbol='+ticker
    web = requests.get(url2)
    soup2 = BeautifulSoup(web.text,'html.parser')
    LTPData = soup2.find_all('div',attrs={'class':'container'})
    for i in LTPData:
        print(i.text)

scrap_procon('TCS')