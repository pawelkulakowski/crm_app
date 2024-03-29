# Generated by Django 3.1.1 on 2020-10-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0024_auto_20201021_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactperson',
            name='default',
            field=models.BooleanField(blank=True, null=True, verbose_name='Kontakt domyślny'),
        ),
        migrations.AddField(
            model_name='historicalcontactperson',
            name='default',
            field=models.BooleanField(blank=True, null=True, verbose_name='Kontakt domyślny'),
        ),
        migrations.AlterField(
            model_name='contactperson',
            name='linkedin_added',
            field=models.BooleanField(blank=True, null=True, verbose_name='Kontakt Linkedin'),
        ),
        migrations.AlterField(
            model_name='historicalcontactperson',
            name='linkedin_added',
            field=models.BooleanField(blank=True, null=True, verbose_name='Kontakt Linkedin'),
        ),
    ]
