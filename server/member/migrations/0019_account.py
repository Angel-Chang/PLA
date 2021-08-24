# Generated by Django 3.0 on 2021-06-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0018_auto_20210614_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('user_account', models.CharField(max_length=20, verbose_name='帳號')),
                ('user_password', models.CharField(max_length=20, verbose_name='密碼')),
                ('user_name', models.CharField(max_length=50, verbose_name='名稱')),
                ('level', models.CharField(choices=[('1', '一般客服'), ('2', '客服主管'), ('8', '系統主管'), ('9', '工程師')], default='8', max_length=1, verbose_name='系統身份')),
                ('create_user', models.CharField(max_length=20, verbose_name='創建者帳號')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_login_date', models.DateTimeField(blank=True, null=True, verbose_name='最後登入時間')),
                ('modify_user', models.CharField(max_length=20, verbose_name='異動者帳號')),
                ('last_modify_date', models.DateTimeField(blank=True, null=True, verbose_name='最後異動時間')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否被刪除')),
                ('deleted_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='刪除者帳號')),
                ('deleted_date', models.DateTimeField(blank=True, null=True, verbose_name='帳號刪除時間')),
            ],
        ),
    ]