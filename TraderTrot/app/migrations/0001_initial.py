# Generated by Django 4.0.1 on 2022-01-15 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='login_tbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('Email', models.CharField(max_length=30)),
                ('ContactNo', models.CharField(max_length=12)),
                ('ExperienceYr', models.CharField(max_length=2)),
                ('Profession', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'login_tbl',
            },
        ),
    ]
