# Generated by Django 3.0 on 2020-02-08 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20200208_0850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='city_id',
            new_name='city',
        ),
    ]
