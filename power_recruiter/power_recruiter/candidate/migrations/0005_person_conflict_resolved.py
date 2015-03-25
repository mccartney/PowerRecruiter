# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0004_auto_20150316_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='conflict_resolved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
