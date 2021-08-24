# Generated by Django 3.0 on 2021-04-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_logininfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_clinic',
            field=models.BooleanField(default=False, verbose_name='診所身份'),
        ),
        migrations.AddField(
            model_name='member',
            name='is_doctor',
            field=models.BooleanField(default=False, verbose_name='醫師身份'),
        ),
        migrations.AddField(
            model_name='member',
            name='is_store',
            field=models.BooleanField(default=False, verbose_name='店家身份'),
        ),
        migrations.AlterField(
            model_name='member',
            name='sex',
            field=models.CharField(blank=True, choices=[('', ''), ('1', '男'), ('2', '女'), ('3', '其他')], default='', max_length=1, null=True, verbose_name='性別'),
        ),
    ]
