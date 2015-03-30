# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_site', '0005_auto_20150316_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='state',
            field=models.ForeignKey(to='basic_site.State', null=True),
        ),
    ]
