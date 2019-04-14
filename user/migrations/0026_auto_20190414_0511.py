# Generated by Django 2.1.7 on 2019-04-14 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_profile_linkedin_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='skype_profile',
            field=models.URLField(blank=True, null=True, verbose_name='Skype Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='spotify_profile',
            field=models.URLField(blank=True, null=True, verbose_name='Spotify Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedin_profile',
            field=models.URLField(blank=True, null=True, verbose_name='Linkedin Profile'),
        ),
    ]
