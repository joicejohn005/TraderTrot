from django.db import models

# Create your models here.
class login_tbl(models.Model):
    Name=models.CharField(max_length=30)
    Email=models.CharField(max_length=30)
    ContactNo=models.CharField(max_length=12)
    ExperienceYr=models.CharField(max_length=2)
    Profession=models.CharField(max_length=30)

    class Meta:
        db_table = "login_tbl"