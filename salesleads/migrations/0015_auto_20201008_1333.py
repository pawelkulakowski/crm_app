# Generated by Django 3.1.1 on 2020-10-08 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0014_auto_20201008_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='latitude',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='longtitude',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='latitude',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='longtitude',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]