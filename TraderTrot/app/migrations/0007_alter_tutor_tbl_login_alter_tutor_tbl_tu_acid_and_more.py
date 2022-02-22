# Generated by Django 4.0.1 on 2022-02-20 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_tradebook_tbl_buy_alter_tradebook_tbl_pnl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor_tbl',
            name='login',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.login_tbl'),
        ),
        migrations.AlterField(
            model_name='tutor_tbl',
            name='tu_acid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.academy_tbl'),
        ),
        migrations.CreateModel(
            name='blog_tbl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btitle', models.CharField(max_length=100)),
                ('bsub', models.CharField(max_length=100)),
                ('bstatus', models.BooleanField(default=True)),
                ('bdate', models.DateField(auto_now_add=True)),
                ('bdesc', models.CharField(max_length=500)),
                ('bthumb', models.CharField(max_length=100)),
                ('b_acid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.academy_tbl')),
                ('b_tid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.tutor_tbl')),
            ],
            options={
                'db_table': 'blog_tbl',
            },
        ),
    ]