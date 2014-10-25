# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0002_auto_20141025_1405'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InternetLocation',
            new_name='Source',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='from_where',
            new_name='source',
        ),
        migrations.AlterField(
            model_name='person',
            name='attachments',
            field=models.ManyToManyField(to=b'candidate.Attachment', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='caveats',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
