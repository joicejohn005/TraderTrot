# Generated by Django 4.0.4 on 2022-06-09 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_alter_useractivity_last_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivity',
            name='industry',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='recommendationKey',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='sector',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='stock',
            field=models.CharField(max_length=50),
        ),
    ]
