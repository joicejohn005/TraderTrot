from ast import Global
from asyncio.windows_events import NULL
from email import message
from django.shortcuts import redirect, render
from django.http import *
from app.models import *
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
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

def ac_reg(request):
    
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
        d = academy_tbl.objects.create(ac_name=acname,ac_yr=acyr,ac_contact=accont,ac_info=acinfo,ac_city=accity,ac_website=acweb,ac_logo=uurl,login=e)
        d.save()

    else:
        return redirect('/ad_ac_reg/')    
    
    return redirect('/ad_acManage/')

def ad_userManage(request):
    userdata=user_tbl.objects.all()
    logindata=login_tbl.objects.all()
    return render(request,'ad_userManage.html',{"b":userdata,"c":logindata})

def ad_acManage(request):
    acdata=academy_tbl.objects.all()
    logindata=login_tbl.objects.all()
    return render(request,'ad_acManage.html',{"a":acdata,"b":logindata})

def ad_home(request):
    return render(request,'ad_home.html')
 
#user
def tradebook(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    return render(request,'tradebook.html')
def tradereport(request):
    return render(request,'tradereport.html')
def user_home(request):
    return render(request,'user_home.html')

#accademy
def acc_addPackage(request):
    return render(request,'acc_addPackage.html')

def addPackage(request):
    p=package_tbl()
    d=academy_tbl()
    p.pkg_name=request.POST.get('acname')
    p.pkg_duration=request.POST.get('sdate')
    p.pkg_price=request.POST.get('mobile')
    p.pkg_desc=request.POST.get('info')
    p.pkg_thumb=request.POST.get('logo')
   
    p.save()

def acc_addTutors(request):
    return render(request,'acc_addTutors.html')

def addTutors(request):
    t=tutor_tbl()
    e=login_tbl()
    e.Unemail=request.POST.get('email')
    data = login_tbl.objects.filter(Unemail=e.Unemail).count()
    if data == 0:
        e.password=request.POST.get('pswd')
        e.status=1
        e.type=4
        e.save()

    t.tu_name=request.POST.get('')
    t.tu_exp=request.POST.get('')
    t.tu_cons=request.POST.get('')
    t.tu_contact=request.POST.get('')
    t.tu_desc=request.POST.get('')
    t.tu_acid=request.POST.get('')
    t.save()

def acc_home(request):
    return render(request,'acc_home.html')

#testing
def clipboard(request):
    return render(request,'clipboard.html')

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
                #id = c.id
                if c.type == 0:
                    id = c.id
                    request.session['id']=id
                    return redirect("/newindex/")
                elif c.type == 1:
                    id = c.id
                    request.session['id']=id
                    return render(request,"ad_home.html")
                elif c.type == 2:
                    id = c.id
                    request.session['id']=id
                    acid=academy_tbl.objects.get(login_id=id)
                    request.session['acname']=acid.ac_name
                    return render(request,"acc_home.html")
                elif c.type == 3:
                    id = c.id
                    request.session['id']=id
                    return render(request,"#")#tutor home
            
            return HttpResponseRedirect('/newindex')
        message="Invalid USername or Password"
        return render(request,"login.html",{"message2":message})

def newindex(request):
    if request.session.is_empty():
      return render(request, 'index.html')
    id = request.session['id']
    data=login_tbl.objects.get(id=id)
    userdata = user_tbl.objects.get(id=data.id)
    request.session['Name']=userdata.Name
    return render(request,"index.html")   

def logout(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/index')
    request.session.flush()
    return HttpResponseRedirect('/index')

def date(request):
    date = datetime.datetime.now().strftime("%b %d %Y")
    datetoday = {'date': date}
    return render(request,"ad_ac_reg.html", {"date":date})