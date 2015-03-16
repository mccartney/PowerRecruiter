# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_auto_20150314_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='contact',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=75, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='goldenline',
            field=models.URLField(unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='linkedin',
            field=models.URLField(unique=True, null=True),
            preserve_default=True,
        ),
    ]
