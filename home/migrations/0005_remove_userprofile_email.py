# Generated by Django 3.0 on 2020-02-08 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_userprofile_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
