# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_site', '0002_auto_20150314_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edge',
            name='state_in',
        ),
        migrations.RemoveField(
            model_name='edge',
            name='state_out',
        ),
        migrations.DeleteModel(
            name='Edge',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
