# Generated by Django 4.0.1 on 2022-02-24 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_doubt_tbl_login_solution_tbl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution_tbl',
            old_name='doubt_id',
            new_name='doubt',
        ),
    ]