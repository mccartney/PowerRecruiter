# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('candidate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='goldenline',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='linkedin',
            field=models.URLField(null=True),
        ),
    ]
