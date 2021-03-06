# Generated by Django 3.0 on 2021-03-20 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='member',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False, verbose_name='UID')),
                ('account', models.CharField(max_length=20, verbose_name='會員帳號')),
                ('real_name', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='會員姓名')),
                ('nick_name', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='會員暱稱')),
                ('idNo', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='身分證號碼')),
                ('email', models.EmailField(blank=True, default='', max_length=200, null=True, verbose_name='Email')),
                ('address', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='住址')),
                ('sex', models.CharField(blank=True, choices=[('', ''), ('F', 'Female'), ('M', 'Male')], default='', max_length=1, null=True, verbose_name='性別')),
                ('myself', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='自我介紹')),
                ('photo', models.CharField(blank=True, default='', max_length=254, null=True, verbose_name='照片')),
                ('user_password', models.CharField(max_length=20, verbose_name='密碼')),
                ('fb_account', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='fb綁定的信箱')),
                ('google_account', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='google綁定的信箱')),
                ('qr_code', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='QR code')),
                ('status', models.CharField(blank=True, default='', max_length=1, null=True, verbose_name='狀態')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_login_date', models.DateTimeField(blank=True, null=True, verbose_name='最後登入時間')),
                ('last_modify_date', models.DateTimeField(blank=True, null=True, verbose_name='最後異動時間')),
            ],
        ),
    ]
