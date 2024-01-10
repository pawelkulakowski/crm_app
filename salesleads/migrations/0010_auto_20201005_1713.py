# Generated by Django 3.1.1 on 2020-10-05 17:13

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0009_plannedactivities'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsaleslead',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='saleslead',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
