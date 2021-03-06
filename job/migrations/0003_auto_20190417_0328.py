# Generated by Django 2.1.7 on 2019-04-17 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20190416_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobadvertisement',
            name='avg_salary',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='Ortalama Maaş'),
        ),
        migrations.AlterField(
            model_name='jobadvertisement',
            name='term',
            field=models.SmallIntegerField(choices=[(1, 'Kısa Dönem'), (2, 'Uzun Dönem'), (3, 'Tek Seferlik'), (4, 'Staj'), (5, 'Remote')], verbose_name='Dönem'),
        ),
        migrations.AlterField(
            model_name='jobadvertisement',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Pozisyon'),
        ),
        migrations.AlterField(
            model_name='jobadvertisement',
            name='type',
            field=models.SmallIntegerField(choices=[(1, 'Firma'), (2, 'Bireysel')], verbose_name='İşveren Tipi'),
        ),
    ]
