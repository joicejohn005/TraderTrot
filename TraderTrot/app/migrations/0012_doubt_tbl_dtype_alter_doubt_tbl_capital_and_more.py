# Generated by Django 4.0.1 on 2022-02-25 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_doubt_tbl_servicetag_doubt_tbl_cagr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doubt_tbl',
            name='dtype',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='capital',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='deadline',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='dthumb',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='exchange',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='risk',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='sector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='doubt_tbl',
            name='stock',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
