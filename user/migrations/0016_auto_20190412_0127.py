# Generated by Django 2.1.7 on 2019-04-11 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20190412_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/defaultuser.jpg', null=True, upload_to='avatars/'),
        ),
    ]
