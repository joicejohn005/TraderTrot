# Generated by Django 4.0.4 on 2022-06-25 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_course_datetime_course_tbl_course_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_tbl',
            name='course_tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.tutor_tbl'),
        ),
    ]
