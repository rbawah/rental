# Generated by Django 3.2.10 on 2021-12-13 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpages', '0003_auto_20211212_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='neighbourhood',
            field=models.CharField(help_text='Which community is the home located?', max_length=200),
        ),
        migrations.AlterField(
            model_name='home',
            name='rent',
            field=models.IntegerField(help_text='Rent amount in $'),
        ),
    ]
