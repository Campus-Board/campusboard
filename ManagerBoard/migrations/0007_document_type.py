# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0006_auto_20141130_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.TextField(default=b'bg-yellow'),
            preserve_default=True,
        ),
    ]
