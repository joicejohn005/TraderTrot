# Generated by Django 4.0.1 on 2022-02-12 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_academy_tbl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academy_tbl',
            name='ac_city',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='academy_tbl',
            name='ac_info',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='academy_tbl',
            name='ac_website',
            field=models.CharField(max_length=30),
        ),
    ]