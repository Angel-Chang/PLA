# Generated by Django 3.0 on 2021-06-27 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0021_auto_20210619_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='dynaPost',
            fields=[
                ('post_id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='貼文ID')),
                ('post_published', models.DateTimeField(blank=True, null=True, verbose_name='發佈時間')),
                ('post_created_at', models.DateTimeField(blank=True, null=True, verbose_name='貼文建立時間')),
                ('post_update_at', models.DateTimeField(blank=True, null=True, verbose_name='貼文最後異動時間')),
                ('post_content', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='標題')),
                ('post_decription', models.TextField(blank=True, default='', null=True, verbose_name='貼文')),
                ('post_picture', models.CharField(blank=True, default='', max_length=254, null=True, verbose_name='照片')),
                ('post_url', models.CharField(blank=True, default='', max_length=254, null=True, verbose_name='貼文url')),
                ('post_like', models.IntegerField(default=0, verbose_name='按讚次數')),
                ('post_views', models.IntegerField(default=0, verbose_name='已讀次數')),
                ('page_provider', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='資料來源')),
                ('page_name', models.CharField(blank=True, default='', max_length=150, null=True, verbose_name='page_name')),
                ('page_icon', models.CharField(blank=True, default='', max_length=254, null=True, verbose_name='page_icon')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='DB建立時間')),
                ('last_modify_date', models.DateTimeField(blank=True, null=True, verbose_name='最後異動時間')),
            ],
        ),
    ]
