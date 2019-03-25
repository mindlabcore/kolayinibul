# Generated by Django 2.1.7 on 2019-03-25 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190324_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='page_header_content',
            field=models.SmallIntegerField(choices=[(1, 'Big Box'), (2, 'First Small Box'), (3, 'Second Small Box')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='active_post',
            field=models.SmallIntegerField(choices=[(1, 'Taslak'), (2, 'Yayında'), (3, 'Arşivlendi'), (4, 'Kaldırıldı')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Post Title'),
        ),
    ]