# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0005_auto_20141216_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
        migrations.AlterField(
            model_name='user',
            name='bluetooth_id',
            field=models.CharField(unique=True, max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(unique=True, max_length=30),
            preserve_default=True,
        ),
    ]
