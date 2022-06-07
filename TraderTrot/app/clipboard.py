import requests
from bs4 import BeautifulSoup

url2 = 'https://www.screener.in/company/TCS/consolidated/'
webpage2 = requests.get(url2) #Request to webpage
soup2 = BeautifulSoup(webpage2.text,'html.parser') #parse text frm website

cmp = []

Piotroski_score = soup2.find_all('div',attrs={'class':'company-ratios'})
for i in Piotroski_score:
    x = i.text.split()
    cmp.append(x[i])
    
print(cmp)
    #rs = cmp[0]
    # ltp = cmp[1]
    # chgp = cmp[2].replace('%', '')