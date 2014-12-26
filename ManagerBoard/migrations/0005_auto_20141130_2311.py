# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0004_auto_20141130_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(default=b'', null=True, upload_to=b'board/images/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
