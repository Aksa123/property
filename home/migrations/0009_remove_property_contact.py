# Generated by Django 3.0 on 2020-02-11 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20200211_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='contact',
        ),
    ]
