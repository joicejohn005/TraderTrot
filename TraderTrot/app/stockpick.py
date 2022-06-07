import requests
import pandas as pd
from datetime import datetime,timedelta

def download_from_url(url):
    r = requests.get(url, allow_redirects=True)
    open(url.split('/')[-1], 'wb').write(r.content)
    return url.split('/')[-1]

def join_2_csv(csv1, csv2, col1, col2, select_cols=[], rename_cols=[]):
    csv1 = download_from_url(csv1)
    csv2 = download_from_url(csv2)
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    df = pd.merge(df1, df2, how='inner', left_on=col1, right_on=col2)
    df = df[select_cols]
    df.columns = rename_cols
    df = df[df[rename_cols[1]] > '0.02']
    df = df.sort_values(by=rename_cols[1], ascending=False)
    return df.reset_index()[rename_cols]

def get_date():
    p = datetime.now()-timedelta(days=1)
    if len(str(p.date().day))==2:
        d=str(p.date().day)
    else:
        d='0'+str(p.date().day)
    y = str(p.date().year)
    if len(str(p.date().month))==2:
        mth=str(p.date().month)
    else:
        mth='0'+str(p.date().month)
    return d+mth+y

vol = 'https://www1.nseindia.com/archives/nsccl/volt/CMVOLT_'+get_date()+'.CSV'
n100 = 'https://www1.nseindia.com/content/indices/ind_nifty100list.csv'
select_cols = ['Symbol', 'Current Day Underlying Daily Volatility (E) = Sqrt(0.995*D*D + 0.005*C*C)',
               'Underlying Annualised Volatility (F) = E*Sqrt(365)']
rename_cols = ['Symbol', 'Daily Vol', 'Yearly Vol']
stock=join_2_csv(vol, n100, select_cols[0], rename_cols[0], select_cols, rename_cols)
volstock=stock.iloc[:20]
volstock.index+=1
print(volstock)