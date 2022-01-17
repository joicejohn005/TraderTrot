from django.shortcuts import render
from django.http import HttpResponse
from app.models import *

# Create your views here.
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

def register(request):
    if request.method=="POST":
        name = request.POST['name'] #to get values by POST method frm form
        email = request.POST['email']
        mobile = request.POST['mobile']
        year = request.POST['year']
        password = request.POST['pswd']
        profession = request.POST['profession']

        #import models from app (line 3)
        data = login_tbl.objects.filter(Unemail=email).count()
        if data == 0:
            login = login_tbl.objects.create(Unemail=email,password=password,status=1,type=0) #a=b,a->coloumn name of corresponding table,b->variable name
            login.save() #saving detals
            userid = login_tbl.objects.get(Unemail=email) #to get id and store to foreignkey values

            user = user_tbl.objects.create(Name=name,ContactNo=mobile,ExperienceYr=year,Profession=profession,login_id=userid.id)
            user.save()
            message="Your registration is successfull"
            return render(request,"login.html",{"message":message})
            