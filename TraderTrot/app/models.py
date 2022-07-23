# from asyncio.windows_events import NULL
from tkinter import CASCADE
from unicodedata import decimal
from django.db import models

# Create your models here.

#creating table in mysql
class login_tbl(models.Model):
    Unemail=models.EmailField(max_length=30)
    password=models.CharField(max_length=30)
    status=models.BooleanField(default=True)
    type=models.IntegerField()
#manually setting table name
    class Meta:
        db_table= "login_tbl"

class user_tbl(models.Model):
    Name=models.CharField(max_length=30)
    ContactNo=models.CharField(max_length=12)
    ExperienceYr=models.CharField(max_length=2)
    Profession=models.CharField(max_length=30)
    trdr_type=models.CharField(max_length=30)
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE) #setting foreign key

    class Meta:
        db_table= "user_tbl"

class academy_tbl(models.Model):
    ac_name=models.CharField(max_length=30)
    ac_yr=models.CharField(max_length=4)
    ac_contact=models.CharField(max_length=12)
    ac_info=models.CharField(max_length=100)
    ac_city=models.CharField(max_length=30)
    ac_website=models.CharField(max_length=30)
    ac_logo=models.CharField(max_length=100)
    ac_date=models.DateField(auto_now_add=True)
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE, null=True) #setting foreign key


    class Meta:
        db_table= "academy_tbl"

class tutor_tbl(models.Model):
    tu_name=models.CharField(max_length=30)
    tu_exp=models.CharField(max_length=4)
    tu_cons=models.CharField(max_length=4)
    tu_contact=models.CharField(max_length=12)
    tu_desc=models.CharField(max_length=100)
    tu_acid=models.ForeignKey(academy_tbl, on_delete=models.CASCADE, null=True)
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table= "tutor_tbl"


class course_tbl(models.Model):
    course_name=models.CharField(max_length=30)
    course_description=models.CharField(max_length=300)
    course_duration=models.CharField(max_length=4)
    course_thumb=models.CharField(max_length=100)
    course_language=models.CharField(max_length=20)
    course_date=models.DateField(auto_now_add=True)
    course_rating=models.DecimalField(max_digits=2, decimal_places=1, default=0)
    
    course_tutor=models.ForeignKey(tutor_tbl, on_delete=models.CASCADE,null=True)
    course_ac=models.ForeignKey(academy_tbl, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table= "course_tbl"

class coursefeature_tbl(models.Model):
    course_feature=models.CharField(max_length=50)
    cf_acid=models.ForeignKey(academy_tbl, on_delete=models.CASCADE,null=True)
    cf_course=models.ForeignKey(course_tbl, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table= "coursefeature_tbl"

class unit_tbl(models.Model):
    u_no=models.IntegerField()
    u_title=models.CharField(max_length=50)
    u_content=models.CharField(max_length=100) #what will u learn | seperate[strip()] with ' , ' 
    u_course=models.ForeignKey(course_tbl, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table= "unit_tbl"

class chapter_tbl(models.Model):
    ch_no=models.IntegerField()
    ch_note=models.CharField(max_length=300)
    ch_videotitle=models.CharField(max_length=100)
    ch_video=models.CharField(max_length=100)
    ch_pdftitle=models.CharField(max_length=100)
    ch_pdf=models.CharField(max_length=100)
    ch_unit=models.ForeignKey(unit_tbl, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table= "chapter_tbl"

class subscription_tbl(models.Model):
    sub_status=models.CharField(max_length=20) #Subscribed,started,finished,unsubscribed
    sub_date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(user_tbl, on_delete=models.CASCADE,null=True)
    course=models.ForeignKey(course_tbl, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table= "subscription_tbl"

class courserating_tbl(models.Model):
    rating=models.IntegerField()
    user_review=models.CharField(max_length=150, null=True)
    course=models.ForeignKey(course_tbl, on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(user_tbl, on_delete=models.CASCADE,null=True)

    class Meta:
        db_table="courserating_tbl"

class tradebook_tbl(models.Model):
    stock=models.CharField(max_length=20)
    qty=models.IntegerField()
    b_date=models.DateField()
    s_date=models.DateField()
    buy=models.DecimalField(max_digits=10, decimal_places=2)
    sell=models.DecimalField(max_digits=10, decimal_places=2)
    pnl=models.DecimalField(max_digits=10, decimal_places=2)
    gain=models.DecimalField(max_digits=5, decimal_places=2,null=True)
    strategy=models.CharField(max_length=100, null=True)
    remark=models.CharField(max_length=100, null=True)
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE) #setting foreign key
    nodays = models.IntegerField()

    class Meta:
        db_table= "tradebook_tbl"

class blog_tbl(models.Model):
    btitle=models.CharField(max_length=100)
    bsub=models.CharField(max_length=100)
    bstatus=models.BooleanField(default=True)
    bdate=models.DateField(auto_now_add=True)
    bdesc=models.CharField(max_length=500)
    bthumb=models.CharField(max_length=100)
    b_acid=models.ForeignKey(academy_tbl, on_delete=models.CASCADE, null=True)
    b_tid=models.ForeignKey(tutor_tbl, on_delete=models.CASCADE, null=True) # foreign key academy

    class Meta:
        db_table= "blog_tbl"

class doubt_tbl(models.Model):
    dtitle=models.CharField(max_length=100) #mandatory
    ddesc=models.CharField(max_length=500) #mandatory
    dtype=models.CharField(max_length=20,default=NULL) #mandatory
    ddate=models.DateField(auto_now_add=True) #mandatory
    dstatus=models.CharField(max_length=10) #mandatory
    dthumb=models.CharField(max_length=100,null=True)
    time=models.CharField(max_length=20, null=True)
    cagr=models.CharField(max_length=20, null=True)
    target=models.CharField(max_length=20, null=True)
    stock=models.CharField(max_length=20,null=True)
    exchange=models.CharField(max_length=20,null=True)
    deadline=models.DateField(null=True,auto_now_add=False,default=None)
    risk=models.CharField(max_length=20,null=True)
    capital=models.CharField(max_length=20,null=True)
    sector=models.CharField(max_length=50,null=True)
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE, null=True) #user

    class Meta:
        db_table= "doubt_tbl"

class solution_tbl(models.Model):
    solution=models.CharField(max_length=500)
    sdate=models.DateField(auto_now_add=True)
    link=models.CharField(max_length=30)
    doubt=models.ForeignKey(doubt_tbl, on_delete=models.CASCADE, null=True)
    login=models.ForeignKey(tutor_tbl, on_delete=models.CASCADE, null=True) #tutor
    ulogin=models.ForeignKey(login_tbl, on_delete=models.CASCADE, null=True) #tutor


    class Meta:
        db_table= "solution_tbl"

class stockdata(models.Model):        
    symbol=models.CharField(max_length=12)
    date=models.DateField(null=False)

    class Meta:
        db_table="stockdata"

class loginactivity(models.Model):
    logintime = models.DateTimeField(auto_now_add=True)
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE, null=True) #setting foreign key

    class Meta:
        db_table="loginactivity"

class useractivity(models.Model):
    login=models.ForeignKey(login_tbl, on_delete=models.CASCADE, null=True) #setting foreign key
    stock=models.CharField(max_length=50)
    date=models.DateField(auto_now_add=True)
    sector=models.CharField(max_length=50)
    industry=models.CharField(max_length=50)
    revenueGrowth=models.DecimalField(max_digits=5, decimal_places=2)
    recommendationKey=models.CharField(max_length=50)
    last_price=models.DecimalField(max_digits=20, decimal_places=2,null=False,default=0.00)

    class Meta:
        db_table="useractivity"