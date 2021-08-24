# Generated by Django 3.0 on 2021-03-24 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_delete_logininfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('account', models.CharField(max_length=100, verbose_name='登入帳號')),
                ('login_type', models.PositiveIntegerField(choices=[(0, '一般登入'), (1, 'google 登入'), (2, 'facebook 登入')], default=0, verbose_name='登入方式')),
                ('login_success', models.BooleanField(default=False, verbose_name='登入成功/失敗')),
                ('message', models.CharField(max_length=200, verbose_name='訊息')),
                ('login_date', models.DateTimeField(auto_now=True, verbose_name='登入時間')),
            ],
        ),
    ]
