# Generated by Django 3.0 on 2020-03-05 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_contactmail'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='main',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
