# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_site', '0004_auto_20150316_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='hired',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='state',
            name='rejected',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
