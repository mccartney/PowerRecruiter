# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.IntegerField()),
                ('state', models.IntegerField()),
                ('message', models.TextField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
