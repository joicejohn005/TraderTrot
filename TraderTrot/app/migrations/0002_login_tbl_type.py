# Generated by Django 4.0.1 on 2022-01-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='login_tbl',
            name='type',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]