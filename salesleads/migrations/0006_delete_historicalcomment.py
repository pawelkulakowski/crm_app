# Generated by Django 3.1.1 on 2020-09-30 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0005_auto_20200930_0809'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalComment',
        ),
    ]