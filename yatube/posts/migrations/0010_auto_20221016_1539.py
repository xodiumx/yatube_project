# Generated by Django 2.2.16 on 2022-10-16 08:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20221014_1831'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': (
                'created',), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='written_at',
        ),
        migrations.RemoveField(
            model_name='post',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='created',
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]
