# Generated by Django 4.0.4 on 2022-06-25 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_course_tbl_course_tutor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_tbl',
            name='course_tutor',
        ),
    ]
