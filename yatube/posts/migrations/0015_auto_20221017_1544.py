# Generated by Django 2.2.16 on 2022-10-17 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20221017_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='currnet_user',
        ),
        migrations.AddField(
            model_name='follow',
            name='current_user',
            field=models.IntegerField(default=None),
        ),
        migrations.RemoveField(
            model_name='follow',
            name='post_author',
        ),
        migrations.AddField(
            model_name='follow',
            name='post_author',
            field=models.IntegerField(default=None),
        ),
    ]