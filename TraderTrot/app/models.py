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