# Generated by Django 3.0 on 2021-03-24 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_logininfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LoginInfo',
        ),
    ]
