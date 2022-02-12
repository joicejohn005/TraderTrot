from ast import Global
from asyncio.windows_events import NULL
from email import message
from django.shortcuts import render
from django.http import *
from app.models import *
import datetime

# Create your views here.
#all user
def index(request):  
    return render (request,'index.html')
def blogs(request):
    return render (request,'blogs.html')
def blog(request):
    return render (request,'blog-details.html') 
def login(request):
    return render (request,'login.html')
def user_reg(request):
    return render (request,'user_reg.html')

#admin  
def ad_ac_reg(request):
    return render(request,'ad_ac_reg.html')
def ad_userManage(request):
    return render(request,'ad_userManage.html')
def ad_acManage(request):
    return render(request,'ad_acManage.html')
def ad_home(request):
    return render(request,'ad_home.html')

#user
def tradebook(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    return render(request,'tradebook.html')
def tradereport(request):
    return render(request,'tradereport.html')

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
     
def checklogin(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['pswd']
        data = login_tbl.objects.filter(Unemail=email,password=password)
        count= data.count()
        if count==1:
            for c in data:
                id = c.id
            request.session['id']=id
            return HttpResponseRedirect('/newindex')
        message="Invalid USername or Password"
        return render(request,"login.html",{"message2":message})

def newindex(request):
    if request.session.is_empty():
      return render(request, 'index.html')
    id = request.session['id']
    data=login_tbl.objects.get(id=id)
    userdata = user_tbl.objects.get(id=data.id)
    return render(request,"index.html",{"username":userdata.Name})   

def logout(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/index')
    request.session.flush()
    return HttpResponseRedirect('/index')

def date(request):
    date = datetime.datetime.now().strftime("%b %d %Y")
    #datetoday = {'date': date}
    return render(request,"ad_ac_reg.html", {"date":date})
