# Generated by Django 2.1.7 on 2019-03-21 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_subcategory_sub_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='sub_category_image',
            field=models.FileField(blank=True, null=True, upload_to='sub_category_images/'),
        ),
    ]
