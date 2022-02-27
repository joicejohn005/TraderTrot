from asyncio.windows_events import NULL
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
    ac_tutorcount=models.CharField(max_length=10)#tutortable
    ac_packagecount=models.CharField(max_length=10)#package table
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

class package_tbl(models.Model):
    pkg_name=models.CharField(max_length=30)
    pkg_duration=models.CharField(max_length=4)
    pkg_thumb=models.CharField(max_length=100)
    pkg_price=models.CharField(max_length=10)
    pkg_desc=models.CharField(max_length=100)
    p_acid=models.ForeignKey(academy_tbl, on_delete=models.CASCADE)

    class Meta:
        db_table= "package_tbl"

class pkgfeature_tbl(models.Model):
    pkg_feature=models.CharField(max_length=50)
    pf_acid=models.ForeignKey(academy_tbl, on_delete=models.CASCADE)
    pf_pkgid=models.ForeignKey(package_tbl, on_delete=models.CASCADE)

    class Meta:
        db_table= "pkgfeature_tbl"

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