# Generated by Django 2.1.7 on 2019-04-11 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20190412_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='/defaultuser.jpg', upload_to='avatars/'),
        ),
    ]