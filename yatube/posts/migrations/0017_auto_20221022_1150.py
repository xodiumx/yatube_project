# Generated by Django 2.2.16 on 2022-10-22 04:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0016_auto_20221017_1717'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',)},
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'author')},
        ),
    ]
