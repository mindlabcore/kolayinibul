# Generated by Django 2.1.7 on 2019-03-16 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20190316_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='post',
            field=models.ManyToManyField(blank=True, to='blog.Post'),
        ),
    ]
