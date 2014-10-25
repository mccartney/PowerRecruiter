# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0003_auto_20141025_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='attachments',
        ),
        migrations.AddField(
            model_name='attachment',
            name='person',
            field=models.ForeignKey(default=1, to='candidate.Person'),
            preserve_default=True,
        ),
    ]
