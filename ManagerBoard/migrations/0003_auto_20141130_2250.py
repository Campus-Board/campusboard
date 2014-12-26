# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0002_auto_20141130_2233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='content',
            new_name='message',
        ),
        migrations.AddField(
            model_name='document',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
