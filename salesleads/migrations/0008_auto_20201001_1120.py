# Generated by Django 3.1.1 on 2020-10-01 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salesleads', '0007_auto_20200930_1956'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='historicalsaleslead',
            name='city',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Miejscowość'),
        ),
        migrations.AddField(
            model_name='historicalsaleslead',
            name='postcode',
            field=models.IntegerField(blank=True, null=True, verbose_name='Kod pocztowy'),
        ),
        migrations.AddField(
            model_name='historicalsaleslead',
            name='street',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Ulica'),
        ),
        migrations.AddField(
            model_name='saleslead',
            name='city',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Miejscowość'),
        ),
        migrations.AddField(
            model_name='saleslead',
            name='postcode',
            field=models.IntegerField(blank=True, null=True, verbose_name='Kod pocztowy'),
        ),
        migrations.AddField(
            model_name='saleslead',
            name='street',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Ulica'),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='brands',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Referencje'),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='company_name',
            field=models.CharField(max_length=65, null=True, verbose_name='Nazwa firmy'),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='company_website',
            field=models.URLField(blank=True, null=True, verbose_name='Strona www'),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='country',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='salesleads.country', verbose_name='Kraj'),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='source',
            field=models.IntegerField(blank=True, choices=[(1, 'targi'), (2, 'internet'), (3, 'linkedin'), (4, 'inne')], null=True, verbose_name='Źródło'),
        ),
        migrations.AlterField(
            model_name='historicalsaleslead',
            name='type',
            field=models.IntegerField(choices=[(1, 'Nowy klient'), (2, 'Rozszerzenie oferty'), (3, 'Historyczny klient')], null=True, verbose_name='Typ'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='brands',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Referencje'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='company_name',
            field=models.CharField(max_length=65, null=True, verbose_name='Nazwa firmy'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='company_website',
            field=models.URLField(blank=True, null=True, verbose_name='Strona www'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='salesleads.country', verbose_name='Kraj'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='source',
            field=models.IntegerField(blank=True, choices=[(1, 'targi'), (2, 'internet'), (3, 'linkedin'), (4, 'inne')], null=True, verbose_name='Źródło'),
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='type',
            field=models.IntegerField(choices=[(1, 'Nowy klient'), (2, 'Rozszerzenie oferty'), (3, 'Historyczny klient')], null=True, verbose_name='Typ'),
        ),
    ]