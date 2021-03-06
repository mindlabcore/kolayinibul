# Generated by Django 2.1.7 on 2019-04-11 22:21

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_subcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='active_post',
            field=models.SmallIntegerField(choices=[(1, 'Taslak'), (2, 'Yayında'), (3, 'Arşivlendi'), (4, 'Kaldırıldı'), (5, 'Onay Bekliyor')], default=5),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Yazar'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='Kategori Adı'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=ckeditor.fields.RichTextField(max_length=100000, verbose_name='Açıklama'),
        ),
        migrations.AlterField(
            model_name='post',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_category', to='blog.SubCategory', verbose_name='Alt Kategori Adı'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Post Başlığı'),
        ),
    ]
