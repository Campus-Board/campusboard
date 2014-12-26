# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0009_auto_20141216_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='dateEnd',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
