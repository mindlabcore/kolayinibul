# Generated by Django 2.1.7 on 2019-03-12 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_subcategory_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='story_images/'),
        ),
    ]
