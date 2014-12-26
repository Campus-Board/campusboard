# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0008_auto_20141214_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='message',
            field=models.TextField(default=b'No message defined'),
            preserve_default=True,
        ),
    ]
