# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagerBoard', '0007_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
