# Generated by Django 3.2.10 on 2021-12-15 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0005_auto_20211214_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homephotos',
            name='slug',
        ),
    ]
