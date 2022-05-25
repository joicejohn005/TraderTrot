from ast import Global
from app.models import *
from asyncio.windows_events import NULL

from bs4 import BeautifulSoup

import csv

from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import *
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from datetime import datetime #service request
import datetime as dt #plotly

from matplotlib import pyplot as plt
from matplotlib.style import context
from matplotlib import ticker

from nsepy import get_history

import pandas as pd
from plotly import express as px
import plotly.offline as opy
from plotly import graph_objs as go
import pdfkit

import requests
from requests.exceptions import ConnectionError

import seaborn as sns
from symtable import Symbol

import urllib.request

import yfinance as yf
#all user


def index(request):
    blogdata=blog_tbl.objects.select_related("b_tid").order_by('-id')[:3]
    return render (request,'index.html',{"blogdata":blogdata})

def blogs(request):
    blogdata=blog_tbl.objects.select_related("b_tid").order_by('-id')
    return render (request,'blogs.html',{"blogdata":blogdata})

def blog(request):
    blogdata=blog_tbl.objects.select_related("b_tid").order_by('-id')
    return render (request,'blog-details.html',{"blogdata":blogdata})

def blogdetails(request,bid):
    bd = blog_tbl.objects.get(id=bid)
    tname = tutor_tbl.objects.get(id=bd.b_tid_id)
    aname = academy_tbl.objects.get(id=bd.b_acid_id)
    return render(request,'blog-details.html',{"blogdata":bd,"tn":tname,"an":aname})

def login(request):
    return render (request,'login.html')

def user_profile(request):
    return render (request,'user_profile.html')


def user_reg(request):
    return render (request,'user_reg.html')

def stockinfo(request):
    context={'list':stocklist()}

    return render (request,'stockinfo.html',context)

def checklogin(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['pswd']
        data = login_tbl.objects.filter(Unemail=email,password=password,status=1)
        count= data.count()
        if count==1:
            for c in data:
                #id = c.id
                if c.type == 0:
                    id = c.id
                    request.session['id']=id
                    uid=user_tbl.objects.get(login_id=id)
                    request.session['uname']=uid.Name
                    return redirect("/user_home/")
                elif c.type == 1:
                    id = c.id
                    request.session['id']=id
                    return redirect("/ad_home/")
                elif c.type == 2:
                    id = c.id
                    request.session['id']=id

                    acid=academy_tbl.objects.get(login_id=id)
                    request.session['acname']=acid.ac_name
                    return redirect("/acc_home/")

                elif c.type == 3:
                    id = c.id
                    request.session['id']=id
                    tid=tutor_tbl.objects.get(login_id=id)
                    request.session['tname']=tid.tu_name
                   
                    return redirect("/tu_home/")
            
            return HttpResponseRedirect('/newindex')
        message="Invalid USername or Password Or Inactive user"
        return render(request,"login.html",{"message2":message})

def newindex(request):
    if request.session.is_empty():
      return render(request, 'index.html')
    id = request.session['id']
    data=login_tbl.objects.get(id=id)
    userdata = user_tbl.objects.get(id=data.id)
    request.session['Name']=userdata.Name
    blogdata=blog_tbl.objects.select_related("b_tid").order_by('-id')[:3]
    return render (request,'index.html',{"blogdata":blogdata})

def logout(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/index')
    request.session.flush()
    return HttpResponseRedirect('/index')

#admin  
def ad_ac_reg(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    return render(request,'ad_ac_reg.html')

def status(request,sid):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    status = login_tbl.objects.get(id=sid)
    status.status = 0
    status.save()
    return redirect('/ad_userManage')

def status2(request,sid):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    status = login_tbl.objects.get(id=sid)
    status.status = 1
    status.save()
    return redirect('/ad_userManage')


def ac_reg(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    e=login_tbl()
    mail=request.POST.get('email')   
    e.Unemail=mail
    data = 0
    data = login_tbl.objects.filter(Unemail=e.Unemail).count()
    acname=request.POST.get('acname')
    acyr=request.POST.get('sdate')
    accont=request.POST.get('mobile')
    acinfo=request.POST.get('info')
    accity=request.POST.get('city')
    acweb=request.POST.get('web')
    pkgcount = 0
    if data == 0:
        e.password=request.POST.get('pswd')
        e.status=1
        e.type=2
        e.save()
        Photo=request.FILES['logo']
        fs=FileSystemStorage()
        fn=fs.save(Photo.name,Photo)
        uploaded_file_url=fs.url(fn)
        uurl=uploaded_file_url
        d = academy_tbl.objects.create(ac_name=acname,ac_yr=acyr,ac_contact=accont,ac_info=acinfo,ac_city=accity,ac_website=acweb,ac_logo=uurl,login=e,ac_packagecount=pkgcount)
        d.save()

    else:
        return redirect('/ad_ac_reg/')
    return redirect('/ad_acManage/')

def ad_acManage(request):
    return redirect('/ad_userManage')

def ad_userManage(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    logindata=login_tbl.objects.all()

    userdata=user_tbl.objects.all()

    acdata=academy_tbl.objects.all()

    tudata=tutor_tbl.objects.all()

    return render(request,'ad_userManage.html',{"a":acdata,"b":userdata,"c":logindata,"t":tudata})

def ad_home(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')

    blogcount = blog_tbl.objects.all().count()
    
    return render(request,'ad_home.html',{"blogc":blogcount})
 
#user
def register(request):
 
    if request.method=="POST":
        name = request.POST['name'] #to get values by POST method frm form
        email = request.POST['email']
        mobile = request.POST['mobile']
        year = request.POST['year']
        password = request.POST['pswd']
        profession = request.POST['profession']

        #import models from app (line 3)
        data = login_tbl.objects.filter(Unemail=email).count() #to get all rows of data use filter
        if data == 0:
            login = login_tbl.objects.create(Unemail=email,password=password,status=1,type=0) #a=b,a->coloumn name of corresponding table,b->variable name
            login.save() #saving detals
            userid = login_tbl.objects.get(Unemail=email) #to get id and store to foreignkey values

            user = user_tbl.objects.create(Name=name,ContactNo=mobile,ExperienceYr=year,Profession=profession,login_id=userid.id)
            user.save()
            message1="Your registration is successfull... Please Login"
            return render(request,"user_reg.html",{"message":message1})
        message2="Email already registered"
        return render(request, 'user_reg.html',{"message":message2})

def user_home(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    blogcount = blog_tbl.objects.all().count()

    id = request.session['id']
    tradedata = tradebook_tbl.objects.filter(login_id=id)
    profit = 0
    for t in tradedata:
        profit = profit + t.pnl

    requestdata = doubt_tbl.objects.filter(login_id=id).count()
    solutioncount= doubt_tbl.objects.filter(login_id=id,dstatus="Finished").count()

    return render(request,'user_home.html',{"blogc":blogcount,"profit":profit,"doubt":requestdata,"sc":solutioncount})

def tradebook(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    id = request.session['id']
    tradedata = tradebook_tbl.objects.select_related('login').filter(login_id=id)
    profit = 0
    for t in tradedata:
        profit = profit + t.pnl
    context={'list':stocklist(),"td":tradedata,"pnl":profit}
    return render(request,'tradebook.html',context)

#pip install pandas
def stocklist():
    df = pd.read_csv('app/equity.csv')
    nselist = df['SYMBOL'].tolist()  #coloumn name :SYMBOL
    return nselist

#pip install wkhtmltopdf
#pip  install csv
def csvd(request):
    id = request.session['id']
    tradedata = tradebook_tbl.objects.filter(login_id=id).order_by('id')
    list = []

    trcolm = ['Stock Name','Quantity','Buy Price','Buy Date','Sell price','Sell Date','Profit n Loss','Remark','Strategy']
    for i in tradedata:
        list1 = [i.stock,i.qty,i.buy,i.b_date,i.sell,i.s_date,i.pnl,i.remark,i.strategy]
        list.append(list1)
        print(list)
        
    with open('tradebook.csv', 'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(trcolm)
        writer.writerows(list)
    return redirect('/tradebook/')

#pip install pdfkit
#pip  install pandas

def pdf(request):
    csvfile = pd.read_csv("tradebook.csv")
    csvfile.to_html("tradebook.html")
    # https://wkhtmltopdf.org/downloads.html
    path_wkhtmltopdf = r'C:\Users\Joice John\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("tradebook.html","tradebook.pdf",configuration=config)
    return redirect('/tradebook/')


def addtrade(request):
    if request.method=="POST":
        stock = request.POST['stock']
        quantity = int(request.POST['qty'])
        entry = float( request.POST['entry'])
        edate = request.POST['edate']
        exit = float( request.POST['exit'])
        exdate = request.POST['exdate']
        pnl = (exit-entry)*quantity
        gain = (pnl / (quantity*entry)) * 100
        strategy = request.POST['strg']
        remark = request.POST['remark'] 

        id = request.session['id']
        
        trade = tradebook_tbl.objects.create(stock=stock,qty=quantity,b_date=edate,s_date=exdate,buy=entry,sell=exit,pnl=pnl,gain=gain,strategy=strategy,remark=remark,login_id=id)
        trade.save()
    return redirect('/tradebook/')
    
def user_request(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    context={'list':stocklist()}
    return render(request,'user_request.html',context)

def invest_req(request):
    if request.method=="POST":
        stock = request.POST['stock']
        exchange = request.POST['stkex']
        subject = request.POST['sub']
        desc = request.POST['remark']     
        
        Photo = request.FILES.get('pic', False)
        if Photo == False:
            uurl=None
        else:    
            fs=FileSystemStorage()
            fn=fs.save(Photo.name,Photo)
            uploaded_file_url=fs.url(fn)
            uurl=uploaded_file_url
              
        deadline=request.POST.get('deadline')
        try:
            datetime.strptime(deadline, '%Y-%m-%d')
            deadline = deadline
        except ValueError:
            deadline = None

        time = request.POST['time']
        cagr = request.POST['cagr']
        target = request.POST['target']

        dtype = "Investing"
        dstatus = "send"

        id = request.session['id']

        doubt = doubt_tbl.objects.create(dtitle=subject,ddesc=desc,dtype=dtype,dstatus=dstatus,dthumb=uurl,time=time,cagr=cagr,target=target,stock=stock,exchange=exchange,deadline=deadline,login_id=id)
        doubt.save()

    return redirect('/user_request/')

def trade_req(request):
    if request.method=="POST":
        stock = request.POST['stock']
        exchange = request.POST['stkex']
        subject = request.POST['sub']
        desc = request.POST['remark']     
        
        Photo = request.FILES.get('pic', False)
        if Photo == False:
            uurl=None
        else:    
            fs=FileSystemStorage()
            fn=fs.save(Photo.name,Photo)
            uploaded_file_url=fs.url(fn)
            uurl=uploaded_file_url
              
        deadline=request.POST.get('deadline')
        try:
            datetime.strptime(deadline, '%Y-%m-%d')
            deadline = deadline
        except ValueError:
            deadline = None

        time = request.POST['time']
        cagr = request.POST['cagr']
        target = request.POST['target']

        dtype = "Trading"
        dstatus = "send"

        id = request.session['id']

        doubt = doubt_tbl.objects.create(dtitle=subject,ddesc=desc,dtype=dtype,dstatus=dstatus,dthumb=uurl,time=time,cagr=cagr,target=target,stock=stock,exchange=exchange,deadline=deadline,login_id=id)
        doubt.save()

    return redirect('/user_request/')

def tips_req(request):
    if request.method=="POST":
        stock = request.POST['stock']
        risk = request.POST['risk']
        subject = request.POST['sub']
        desc = request.POST['remark']
        cap = request.POST['cap']

        time = request.POST['time']
        cagr = request.POST['cagr']
        target = request.POST['target']

        dtype = "Tips"
        dstatus = "send"

        id = request.session['id']

        doubt = doubt_tbl.objects.create(dtitle=subject,ddesc=desc,dtype=dtype,dstatus=dstatus,stock=stock,time=time,cagr=cagr,target=target,risk=risk,capital=cap,login_id=id)
        doubt.save()

    return redirect('/user_request/')

def other_req(request):
    if request.method=="POST":
        risk = request.POST['risk']
        subject = request.POST['sub']
        desc = request.POST['remark']

        time = request.POST['time']
        cagr = request.POST['cagr']
        target = request.POST['target']

        dtype = "General Doubt"
        dstatus = "send"

        id = request.session['id']

        doubt = doubt_tbl.objects.create(dtitle=subject,ddesc=desc,dtype=dtype,dstatus=dstatus,risk=risk,time=time,cagr=cagr,target=target,login_id=id)
        doubt.save()
    return redirect('/user_request/')
        

def user_reqmanage(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    id=request.session['id']    
    requestdata = doubt_tbl.objects.filter(login_id=id)
    solution = solution_tbl.objects.select_related('doubt').filter(ulogin_id=id)
    
    return render(request,'user_reqmanage.html',{"ureq":requestdata,"sol":solution})

def user_reqdetails(request,id):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    reqdetail = doubt_tbl.objects.get(id=id)
    return render(request,'user_reqdetails.html',{"reqdet":reqdetail})

def deletereq(request):
    if request.method=="POST":
        doubtid = request.POST['doubtid']
        dltreq = doubt_tbl.objects.get(id=doubtid)
        dltreq.delete()
        return redirect('/user_reqmanage/')

def user_reqsolution(request,id):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')

    solution = solution_tbl.objects.select_related('doubt','login','ulogin').filter(id=id)
    for s in solution:
        break
    userdet = user_tbl.objects.filter(login_id=s.ulogin.id)
    return render(request,'user_reqsolution.html',{"sol":solution,"name":userdet})

#accademy
def acc_addPackage(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    return render(request,'acc_addPackage.html')

def accheader(request):

    id = request.session['id']
    name = academy_tbl.objects.get(ac_name=id)
    return render(request,'acc_header.html',{"name":name})

def addPackage(request):
    if request.method=="POST":
        pkg_name=request.POST['pname']
        pkg_duration=request.POST['pmonth']
        Photo=request.FILES['pfile']

        fs=FileSystemStorage()
        fn=fs.save(Photo.name,Photo)
        uploaded_file_url=fs.url(fn)
        uurl=uploaded_file_url
        pkg_price=request.POST['pprice']
        pkg_desc=request.POST['info']

        id = request.session['id']
        acid = academy_tbl.objects.get(login_id=id)
        p = package_tbl.objects.create(pkg_name=pkg_name,pkg_duration=pkg_duration,pkg_price=pkg_price,pkg_desc=pkg_desc,pkg_thumb=uurl,p_acid_id=acid.id)
        p.save()

        return redirect('/acc_addPackage/')

def acc_addTutors(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    return render(request,'acc_addTutors.html')

def addTutors(request):
    e = login_tbl()
    if request.method=="POST":
        tcname = request.POST['tcname']
        temail = request.POST['temail']
        tpswd = request.POST['tpswd']
        texp = request.POST['texp']
        tmobile = request.POST['tmobile']
        tcity = request.POST['tcity']
        tinfo = request.POST['tinfo']
        
        data = login_tbl.objects.filter(Unemail=temail).count() #to get all rows of data use filter
        if data == 0:
            e.Unemail = temail
            e.password = tpswd
            e.status = 1
            e.type=3
            e.save()
        else :
            messages.success(request,"Email Already registered")
            return render(request,'acc_addTutors.html')
        id = request.session['id'] #to know which academy is adding
        acc = academy_tbl.objects.get(login_id=id)
        tutor = tutor_tbl.objects.create(tu_name=tcname,tu_exp=texp,tu_contact=tmobile,tu_cons=tcity,tu_desc=tinfo,login=e,tu_acid_id=acc.id)
        tutor.save()
    return redirect('/acc_addTutors/')

def acc_tutorManage(request):
    tutordata=tutor_tbl.objects.all()
    return render(request,'acc_addTutors.html',{"a":tutordata})

def acc_home(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')

    blogcount = blog_tbl.objects.all().count()
    return render(request,'acc_home.html',{"blogc":blogcount})

#tutor activities
def tu_addBlog(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    return render(request,'tu_addBlog.html')

def tu_home(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')
    count = doubt_tbl.objects.filter(dstatus='send').count()
    count2 = doubt_tbl.objects.filter(dstatus='Viewed').count()
    blogcount = blog_tbl.objects.all().count()
    return render(request,'tu_home.html',{"count":count,"view":count2,"blogc":blogcount})

def addblog(request):

    if request.method=="POST":
        title = request.POST['title']
        sub = request.POST['sub']
        content = request.POST['content']
        Photo=request.FILES['logo']

        fs=FileSystemStorage()
        fn=fs.save(Photo.name,Photo)
        uploaded_file_url=fs.url(fn)
        url = uploaded_file_url
        status = 1

        id = request.session['id']   
        tutor=tutor_tbl.objects.get(login_id=id)
        
        b = blog_tbl.objects.create(btitle=title,bsub=sub,bdesc=content,bthumb=url,bstatus=status,b_tid_id=tutor.id,b_acid_id=tutor.tu_acid_id)
        b.save()

    return redirect('/tu_addBlog/')


def tu_dbtlist(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    users = user_tbl.objects.all()
    doubtlist = doubt_tbl.objects.all()
    return render(request,'tu_dbtlist.html',{"dbt":doubtlist,"user":users})

def tu_dbtdetails(request,id):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
 
    dbtdetails = doubt_tbl.objects.get(id=id)
    name = user_tbl.objects.get(login_id=dbtdetails.login_id)
    return render(request,'tu_dbtdetails.html',{"dbtdetails":dbtdetails,"name":name})

def markview(request,did):
    sts = doubt_tbl.objects.get(id=did)
    sts.dstatus='Viewed'
    sts.save()
    return redirect(tu_dbtdetails,id=did)

def markpro(request,did):
    sts = doubt_tbl.objects.get(id=did)
    sts.dstatus='Processed'
    sts.save()
    return redirect(tu_dbtdetails,id=did)

def solution(request):
    if request.method=="POST":
        solution = request.POST['remark']
        website = request.POST['qty']
        dbtid = request.POST['solid']

        id = request.session['id']   
        tut = tutor_tbl.objects.get(login_id=id)
        ulogin = doubt_tbl.objects.get(id=dbtid)
        sol = solution_tbl.objects.create(solution=solution,link=website,doubt_id=dbtid,login_id=tut.id,ulogin_id=ulogin.login_id)
        sol.save()
    
        sts = doubt_tbl.objects.get(id=dbtid)
        sts.dstatus='Finished'
        sts.save()
    
    return redirect('/tu_dbtlist/')

#testing
def clipboard(request):
    return render(request,'clipboard.html')
     
def date(request):
    date = datetime.datetime.now().strftime("%b %d %Y")
    datetoday = {'date': date}
    return render(request,"ad_ac_reg.html", {"date":date})

#pip install plotly
#pip install nsepy - to get the function get_history

def plot(request):
    if request.method=="POST":
        symbol = request.POST['stock'] 
    else:
        symbol = "TCS"
    start=dt.date(2015,1,1)
    end=dt.date.today()
    data = get_history(symbol = symbol,start=start,end=end) #fn in nsepy; library
    data.to_csv("stock.csv")
    df=pd.read_csv("stock.csv")
    #data1=df.filter(['Close'])
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    div=opy.plot(fig,auto_open=False,output_type='div') #to convert to offline candlestick chart
    context={'graph':div,'list':stocklist()}
    return render(request,'plot.html',context)


def scrap_procon(ticker2):
    url = 'https://www.screener.in/company/' +ticker2+ '/consolidated/'
    webpage = requests.get(url) #Request to webpage
    soup = BeautifulSoup(webpage.text,'html.parser') #parse text frm website

    proslist = []
    conslist = []

    prosText = soup.find_all('div',attrs={'class':'pros'})
    for i in prosText:
        pros = i.text.split('. ')
    
    for j in pros: 
        j = j.replace("Pros","")
        proslist.append(j)

    consText = soup.find_all('div',attrs={'class':'cons'})
    for i in consText:
        cons = i.text.split('. ')

    for k in cons: 
        k = k.replace("Cons","")
        conslist.append(k)
    
    return proslist,conslist

def stockanalysis(request):
    if request.method=="POST":

        ticker = request.POST['stock']+".NS"
        ticker2 = request.POST['stock']

        longName = yf.Ticker(ticker).info['longName']
        sector = yf.Ticker(ticker).info['sector']
        industry = yf.Ticker(ticker).info['industry']
        website = yf.Ticker(ticker).info['website']
        logo_url = yf.Ticker(ticker).info['logo_url']
        longBusinessSummary = yf.Ticker(ticker).info['longBusinessSummary']

        a, b = scrap_procon(ticker2)
        l=a[0].split("\n")
        l=[i for i in l if i]

        m=b[0].split("\n")
        m=[j for j in m if j]


    context={'list':stocklist(),'a':l,'b':m,'shortName':longName,'sector':sector,'industry':industry,'website':website,'logo_url':logo_url,'longBusinessSummary':longBusinessSummary}
    return render(request,'stockinfo.html',context)