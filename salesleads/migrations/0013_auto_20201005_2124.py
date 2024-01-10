# Generated by Django 3.1.1 on 2020-10-05 21:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0012_auto_20201005_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactperson',
            name='user',
        ),
        migrations.RemoveField(
            model_name='historicalcontactperson',
            name='user',
        ),
        migrations.AddField(
            model_name='plannedactivities',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]