# Generated by Django 2.1.7 on 2019-04-11 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=55, null=True),
        ),
    ]