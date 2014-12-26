# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0005_auto_20141130_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(default=b'', null=True, upload_to=b'board/images/%Y/%m/%d', blank=True),
            preserve_default=True,
        ),
    ]
