# Generated by Django 3.1.1 on 2020-10-21 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0023_auto_20201020_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsaleslead',
            name='potential',
            field=models.IntegerField(blank=True, choices=[(1, 'do 5.000 Eur'), (2, '5.000 - 10.000 Eur'), (3, '10.000 - 25.000 Eur'), (4, '25.000 - 50.000 Eur'), (5, '50.000 - 75.000 Eur'), (6, '75.000 - 100.000 Eur'), (7, '100.000 - 125.000 Eur'), (8, '125.000 - 150.000 Eur'), (9, '150.000 - 200.000 Eur'), (10, '200.000 - 250.000 Eur'), (11, 'Powyżej 250.000 Eur')], null=True, verbose_name='Potencjał'),
        ),
        migrations.AddField(
            model_name='saleslead',
            name='potential',
            field=models.IntegerField(blank=True, choices=[(1, 'do 5.000 Eur'), (2, '5.000 - 10.000 Eur'), (3, '10.000 - 25.000 Eur'), (4, '25.000 - 50.000 Eur'), (5, '50.000 - 75.000 Eur'), (6, '75.000 - 100.000 Eur'), (7, '100.000 - 125.000 Eur'), (8, '125.000 - 150.000 Eur'), (9, '150.000 - 200.000 Eur'), (10, '200.000 - 250.000 Eur'), (11, 'Powyżej 250.000 Eur')], null=True, verbose_name='Potencjał'),
        ),
    ]
