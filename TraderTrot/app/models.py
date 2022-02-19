from tkinter import CASCADE
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
    #Email=models.EmailField(max_length=30)
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
    ac_date=models.DateField()

    class Meta:
        db_table= "academy_tbl"