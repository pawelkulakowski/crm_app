# Generated by Django 3.1.1 on 2020-09-30 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0004_auto_20200930_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='type',
            field=models.IntegerField(choices=[(1, 'Nowy klient'), (2, 'Rozszerzenie oferty'), (3, 'Historyczny klient')], null=True),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='type',
            field=models.IntegerField(choices=[(1, 'Nowy klient'), (2, 'Rozszerzenie oferty'), (3, 'Historyczny klient')], null=True),
        ),
    ]
