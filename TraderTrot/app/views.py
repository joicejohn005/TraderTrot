from decimal import Decimal
from app.models import *
from ast import Global
from asyncio.windows_events import NULL

from bs4 import BeautifulSoup

import csv

from datetime import datetime,timedelta #service request
import datetime as dt #plotly
from datetime import date
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Q
from django.http import *
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_control

import io

from keras.models import Sequential
from keras.layers import Dense, LSTM

from matplotlib import pyplot as plt
from matplotlib.style import context
from matplotlib import ticker
from .models import stockdata 

from nsepy import get_history
import numpy as np

import pandas as pd
import pdfkit
from plotly import express as px
import plotly.offline as opy
from plotly import graph_objs as go
import plotly.graph_objects as go

import requests
from requests.exceptions import ConnectionError
import re

import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import statistics
from symtable import Symbol

import TraderTrot.settings

import urllib.request
import urllib,base64

import yfinance as yf

import json
# Create your views here.
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
    id = request.session['id']
    login = user_tbl.objects.get(login=id)
    utype = login.trdr_type
    context={'list':stocklist(),'utype':utype}
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

def forgot(request):
    return render (request,'forgot.html')

def pswdreset(request):
    if request.method=="POST":
        email = request.POST['email']
        em = login_tbl.objects.filter(Unemail=email)
        for i in em:
            if i.Unemail != email:
                alert2="Enter Registered Email"
                return render(request,"forgot.html",{"message":alert2})
            else:
                subject = "TraderTrot Password Reset Mail"
                fromemail = TraderTrot.settings.EMAIL_HOST_USER
                message = f'Your password reset link: \n http://127.0.0.1:8000/resetpswd/ '
                reciept = [email]
                send_mail(subject, fromemail, message, reciept)
                alert = "Check your Registered mail"                   
                return render(request,"login.html",{"message":alert})

def resetpswd(request,sid):
     if request.method=="POST":
        pswd = request.POST['pswd']
        cpswd = request.POST['cpswd']
        upswd = login_tbl.objects.get(id=sid)



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

def numOfDays(date1, date2):
	return (date2-date1).days

def tr_count(list1, l, r):
    return len(list(x for x in list1 if l <= x <= r)) 

import datetime
def addtrade(request):
    if request.method=="POST":
        stock = request.POST['stock']
        quantity = int(request.POST['qty'])
        entry = float( request.POST['entry'])
        exit = float( request.POST['exit'])
        edate = request.POST['edate']
        exdate = request.POST['exdate']
        strategy = request.POST['strg']
        remark = request.POST['remark']
        pnl = (exit-entry)*quantity
        gain = (pnl / (quantity*entry)) * 100

        format = '%Y-%m-%d'

        edat = datetime.datetime.strptime(edate, format) 
        edate1=edat.date()  
        exdat = datetime.datetime.strptime(exdate, format) 
        exdate1=exdat.date() 
        
        id = request.session['id']
        nodays = numOfDays(edate1, exdate1)
        
        trade = tradebook_tbl.objects.create(stock=stock,nodays=nodays,qty=quantity,b_date=edate,s_date=exdate,buy=entry,sell=exit,pnl=pnl,gain=gain,strategy=strategy,remark=remark,login_id=id)
        trade.save()

        day_list = []
        days = tradebook_tbl.objects.filter(login=id)
        for d in days:
            day_list.append(d.nodays)

        l = 0
        r = 0
        l2 = 1
        r2 = 90
        l3= 91
        r3=732
        l4=733
        r4 = 40000
        countlist = []
        x= tr_count(day_list, l, r)
        y= tr_count(day_list, l2, r2)
        z= tr_count(day_list, l3, r3)
        w = tr_count(day_list, l4, r4)

        countlist.append(x)
        countlist.append(y)
        countlist.append(z)
        countlist.append(w)

        trdr_type = ["Day Trader","Swing Trader","Positional Trader","Investor"]

        x = max(countlist)
        if (x == countlist[0]):
            ttype = trdr_type[0]

        elif (x == countlist[1]):
            ttype = trdr_type[1]
        
        elif (x == countlist[2]):
            ttype = trdr_type[2]

        elif (x == countlist[3]):
            ttype = trdr_type[3]

        utype = user_tbl.objects.get(login=id)
        utype.trdr_type=ttype
        utype.save()

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
     
def date1(request):
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
    
    # url2 = 'https://www.screener.in/company/'+ticker2+'/consolidated/'
    # webpage2 = requests.get(url2) #Request to webpage
    # soup2 = BeautifulSoup(webpage2.text,'html.parser') #parse text frm website

    # cmp = []
    # chgp = []

    # LTPData = soup2.find_all('div',attrs={'class':'flex flex-align-center'})
    # for i in LTPData:
    #     x = i.text.split()
    #     cmp.append(x[0])
    #     cmp.append(x[1])
    #     cmp.append(x[2])

    #     #rs = cmp[0]
    #     ltp = cmp[1]
    #     chgp = cmp[2].replace('%', '')
    return proslist,conslist
    # ltp,chgp

def stockanalysis(request):
    if request.session.is_empty():
        return HttpResponseRedirect('login/')  
    else:
        id=request.session['id']  
        if request.method=="POST":

            ticker = request.POST['stock']+".NS"
            ticker2 = request.POST['stock']

            open = yf.Ticker(ticker).info['open']
            volume = yf.Ticker(ticker).info['volume']

            dayLow=yf.Ticker(ticker).info['dayLow']
            dayHigh=yf.Ticker(ticker).info['dayHigh']

            currentPrice=yf.Ticker(ticker).info['currentPrice']

            fiftyTwoWeekHigh=yf.Ticker(ticker).info['fiftyTwoWeekHigh']
            fiftyTwoWeekLow=yf.Ticker(ticker).info['fiftyTwoWeekLow']

            previousClose=yf.Ticker(ticker).info['previousClose']
            d=currentPrice-previousClose
            p=(d/previousClose)*100
            p=round(p, 2)

            longName = yf.Ticker(ticker).info['longName']

            sector = yf.Ticker(ticker).info['sector']
            industry = yf.Ticker(ticker).info['industry']

            website = yf.Ticker(ticker).info['website']
            logo_url = yf.Ticker(ticker).info['logo_url'] 
            longBusinessSummary = yf.Ticker(ticker).info['longBusinessSummary']

#**************************************************************************************************************************#
            # yf_period   = "5y"   # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
            # yf_interval = "1d"    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

            # # print close prices
            # yf_returns = yf.download(
            #         tickers = ticker,       # tickers list or string as well
            #         period = yf_period,      # optional, default is '1mo'
            #         interval = yf_interval,  # fetch data by intervaal
            #         group_by = 'ticker',     # group by ticker
            #         auto_adjust = True,      # adjust all OHLC (open-high-low-close)
            #         prepost = True,          # download market hours data
            #         threads = True,          # threads for mass downloading
            #         proxy = None)            # proxy

            # yf_returns = yf_returns.iloc[:, yf_returns.columns.get_level_values(0)=='Close']

            # yf_divdend = pd.DataFrame()   # initialize dataframe
            # for i in ticker:
            #     x = pd.DataFrame(yf.Ticker(i).dividends)
            #     yf_divdend = pd.concat([yf_divdend,x], axis=1) 
            # yf_divdend = yf_divdend[yf_divdend.index >= yf_returns.index[0]]
            # print(yf_divdend.tail(21))
            # dividend=yf_divdend.tail(21)
            # json_records = dividend.reset_index().to_json(orient ="records")
            # data = json.loads(json_records)

#**************************************************************************************************************************#
            a, b = scrap_procon(ticker2)
            l=a[0].split("\n")
            l=[i for i in l if i]

            m=b[0].split("\n")
            m=[j for j in m if j]

            user_activity(ticker,id)
            context2=stock_prediction(ticker2)

            # slist=[]

            # similar =  useractivity.objects.filter(sector=sector,industry=industry).exclude(stock=ticker2)
            # for i in similar:
            #     slist.append(i.stock)
            report=test(sector,industry,ticker2,id)    
                
        context={'list':stocklist(),'a':l,'b':m,'percentage':p,'longName':longName,'sector':sector,'industry':industry,
                'volume':volume,'open':open,'website':website,'logo_url':logo_url,'longBusinessSummary':longBusinessSummary,
                'dayLow':dayLow,'dayHigh':dayHigh,'currentPrice':currentPrice,'fiftyTwoWeekHigh':fiftyTwoWeekHigh,
                'fiftyTwoWeekLow':fiftyTwoWeekLow,'previousClose':previousClose,'report':report
                }
        context3=context|context2

        return render(request,'stockinfo.html',context3)

def stock_prediction(symbol):
        import datetime 
        
        stock=stockdata()
        import math
        start=datetime.date(2020,1,1)
        end=datetime.date.today()
        st=stockdata.objects.filter(symbol=symbol)
        loc=f"stockdata/{symbol}.csv"
        
        if st.count()==1:
            for i in st:
                if i.date==datetime.date.today():
                    pass
                else:
                    df=pd.read_csv(loc)
                    lastdate=datetime.datetime.strptime(df['Date'].max(),"%Y-%m-%d")
                    print(type(lastdate))
                    start=lastdate.date()+datetime.timedelta(days = 1)
                    data=get_history(symbol=symbol, start=start , end=end)
                    data.to_csv(loc,mode='a',index=True,header=False)
                    i.date=datetime.date.today()
                    i.save()
                    
        else:
            data=get_history(symbol=symbol, start=start , end=end)
            data.to_csv(loc)
            stock.symbol=symbol
            stock.date=datetime.date.today()
            stock.save()
            
               
        df=pd.read_csv(loc)
        df=df.set_index('Date')
        data=df.filter(["Close"])
        dataset=data.values
        training_data_len=math.ceil(len(dataset)*0.8)
        scaler=MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(dataset)
        train_data=scaled_data[0:training_data_len,:]
        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        model = Sequential()
        model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences = False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        model.fit(x_train, y_train, batch_size = 1, epochs = 1)
        test_data = scaled_data[training_data_len - 60: , :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range (60, len(test_data)):
             x_test.append(test_data[i - 60:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid.insert(1,'predictions',predictions)
        last_60_days = data[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)
        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1], 1))
        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = train.index, y = train['Close'],
                            mode='lines',
                            name='Close',
                            marker_color = '#1F77B4'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid['Close'],
                            mode='lines',
                            name='Val',
                            marker_color = '#FF7F0E'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid.predictions,
                            mode='lines',
                            name='Predictions',
                            marker_color = '#2CA02C'))

        fig.update_layout(
            title=symbol,
            titlefont_size = 28,
            hovermode = 'x',
            xaxis = dict(
                title='Date',
                titlefont_size=16,
                tickfont_size=14),
            
            height = 600,
            
            yaxis=dict(
                title='Close price in INR (₹)',
                titlefont_size=16,
                tickfont_size=14),
            legend=dict(
                y=0,
                x=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'))

        div=opy.plot(fig,auto_open=False,output_type='div')
        nse_list=stocklist()
        context2={'list2':nse_list,'graph':div,'price':pred_price}
        return context2

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
    p = dt.datetime.now()-timedelta(days=1)
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

def tradestock(request):

    vol = 'https://www1.nseindia.com/archives/nsccl/volt/CMVOLT_'+get_date()+'.CSV'
    n100 = 'https://www1.nseindia.com/content/indices/ind_nifty100list.csv'
    select_cols = ['Symbol', 'Current Day Underlying Daily Volatility (E) = Sqrt(0.995*D*D + 0.005*C*C)',
                'Underlying Annualised Volatility (F) = E*Sqrt(365)']
    rename_cols = ['Symbol', 'DailyVol', 'YearlyVol']
    stock=join_2_csv(vol, n100, select_cols[0], rename_cols[0], select_cols, rename_cols)
    volstock=stock.iloc[:20]
    volstock.index+=1
    print(volstock.columns)
    json_records = volstock.reset_index().to_json(orient ='records')
    data = json.loads(json_records)
    context = {'d': data}
    # print(volstock)
    return render(request,'tradestock.html',context)

def user_activity(ticker,id):
        # id=request.session['id']
        sector = yf.Ticker(ticker).info['sector']
        industry = yf.Ticker(ticker).info['industry']
        revenueGrowth = yf.Ticker(ticker).info['revenueGrowth']
        recommendationKey = yf.Ticker(ticker).info['recommendationKey']
        currentPrice=yf.Ticker(ticker).info['currentPrice']


        ticker=ticker.replace(".NS","")
        date=datetime.date.today()
        check = useractivity.objects.filter(login_id=id,stock=ticker,date=date)
        if check.count() == 0:
            user_activity=useractivity.objects.create(login_id=id,last_price=currentPrice,stock=ticker,sector=sector,industry=industry,revenueGrowth=revenueGrowth,recommendationKey=recommendationKey)
            user_activity.save()
        else:
            pass    
def test(sector,industry,stock,id):
    slist=[]
    print(sector)
    print(industry)
    print(stock)
    print(id)
    similar =  useractivity.objects.filter(sector=sector,industry=industry,login_id=id).exclude(stock=stock)
    for i in similar:
        print(i.stock)
        if i.stock not in slist:
            slist.append(i.stock)
    print(slist)
    report = []
    print(len(slist))
    for i in slist: 
        revenue =  useractivity.objects.filter(stock=i,login_id=id).order_by('date')[:1]
        for rev in revenue:
        
            ticker = [i+".NS"]
            ticker2=[i]
        
            sdate=rev.date

            last_price=rev.last_price
            currentPrice=yf.Ticker(ticker[0]).info['currentPrice']
            print(currentPrice)

            currentPrice=Decimal(currentPrice)
            currentPrice=round(currentPrice,2)
            pr_chg= currentPrice-last_price
            print(round(pr_chg, 2))
            prchange=round(pr_chg, 2)
            pr_chg_ptg=(pr_chg/last_price)*100
            pr_chg_ptg=round(pr_chg_ptg, 2)

            vdict= {}
            vdict['stock']=i
            vdict['date']=sdate
            vdict['previousprice']=last_price
            vdict['currentprice']=currentPrice
            vdict['prchange']=prchange
            vdict['pr_chg_ptg']=pr_chg_ptg
            vdict['recommendationKey']=rev.recommendationKey

            report.append(vdict)
    return report    

    #return render(request,'clipboard.html')
def test2(request):
    slist=[]
   
    similar =  useractivity.objects.filter(sector='Technology',industry='Information Technology Services',login_id=1).exclude(stock='INFY')
    for i in similar:
        print(i.stock)
        if i.stock not in slist:
            slist.append(i.stock)
    print(slist)
    report = []
    for i in slist: 
        print(i)
        revenue =  useractivity.objects.filter(stock=i,login_id=1).order_by('date')[:1]
        
        for rev in revenue:   
            ticker = [i+".NS"]
            ticker2=[i]
            print(ticker)
            sdate=rev.date
            print(sdate)
            last_price=rev.last_price
            currentPrice=yf.Ticker(ticker[0]).info['currentPrice']
            print(currentPrice)

            currentPrice=Decimal(currentPrice)
            currentPrice=round(currentPrice,2)
            pr_chg= currentPrice-last_price
            print(round(pr_chg, 2))
            prchange=round(pr_chg, 2)
            pr_chg_ptg=(pr_chg/last_price)*100
            pr_chg_ptg=round(pr_chg_ptg, 2)

            vdict= {}
            vdict['stock']=i
            vdict['date']=sdate
            vdict['previousprice']=last_price
            vdict['currentprice']=currentPrice
            vdict['prchange']=prchange
            vdict['pr_chg_ptg']=pr_chg_ptg
            vdict['recommendationKey']=rev.recommendationKey

            report.append(vdict)
    print(report)
    #return report    

    return render(request,'clipboard.html')

def predict(request):
    import datetime 
    if request.method=="POST":
        symbol = request.POST['stock']
        stock=stockdata()
        import math
        start=datetime.date(2020,1,1)
        end=datetime.date.today()
        st=stockdata.objects.filter(symbol=symbol)
        loc=f"stockdata/{symbol}.csv"
        
        if st.count()==1:
            for i in st:
                if i.date==datetime.date.today():
                    pass
                else:
                    df=pd.read_csv(loc)
                    lastdate=datetime.datetime.strptime(df['Date'].max(),"%Y-%m-%d")
                    print(type(lastdate))
                    start=lastdate.date()+datetime.timedelta(days = 1)
                    data=get_history(symbol=symbol, start=start , end=end)
                    data.to_csv(loc,mode='a',index=True,header=False)
                    i.date=datetime.date.today()
                    i.save()
                    
        else:
            data=get_history(symbol=symbol, start=start , end=end)
            data.to_csv(loc)
            stock.symbol=symbol
            stock.date=datetime.date.today()
            stock.save()
            
                
        df=pd.read_csv(loc)
        df=df.set_index('Date')
        data=df.filter(["Close"])
        dataset=data.values
        training_data_len=math.ceil(len(dataset)*0.8)
        scaler=MinMaxScaler(feature_range=(0,1))
        scaled_data=scaler.fit_transform(dataset)
        train_data=scaled_data[0:training_data_len,:]
        x_train = []
        y_train = []
        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        model = Sequential()
        model.add(LSTM(50, return_sequences = True, input_shape = (x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences = False))
        model.add(Dense(25))
        model.add(Dense(1))
        model.compile(optimizer = 'adam', loss = 'mean_squared_error')
        model.fit(x_train, y_train, batch_size = 1, epochs = 1)
        test_data = scaled_data[training_data_len - 60: , :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range (60, len(test_data)):
                x_test.append(test_data[i - 60:i, 0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid.insert(1,'predictions',predictions)
        last_60_days = data[-60:].values
        last_60_days_scaled = scaler.transform(last_60_days)
        X_test = []
        X_test.append(last_60_days_scaled)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1], 1))
        pred_price = model.predict(X_test)
        pred_price = scaler.inverse_transform(pred_price)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = train.index, y = train['Close'],
                            mode='lines',
                            name='Close',
                            marker_color = '#1F77B4'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid['Close'],
                            mode='lines',
                            name='Val',
                            marker_color = '#FF7F0E'))
        fig.add_trace(go.Scatter(x = valid.index, y = valid.predictions,
                            mode='lines',
                            name='Predictions',
                            marker_color = '#2CA02C'))

        fig.update_layout(
            title=symbol,
            titlefont_size = 28,
            hovermode = 'x',
            xaxis = dict(
                title='Date',
                titlefont_size=16,
                tickfont_size=14),
            
            height = 600,
            
            yaxis=dict(
                title='Close price in INR (₹)',
                titlefont_size=16,
                tickfont_size=14),
            legend=dict(
                y=0,
                x=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'))

        div=opy.plot(fig,auto_open=False,output_type='div')
        nse_list=stocklist()
        context2={'list2':nse_list,'graph':div,'price':pred_price}
        # return context2
        return render(request,'stockinfo.html',context2)
    return render(request,'stockinfo.html')