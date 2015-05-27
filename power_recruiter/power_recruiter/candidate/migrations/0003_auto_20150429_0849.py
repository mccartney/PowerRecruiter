# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('candidate', '0002_auto_20150413_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolvedConflict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('person_one', models.ForeignKey(related_name=b'person_one',
                                                 to='candidate.Person')),
                ('person_two', models.ForeignKey(related_name=b'person_two',
                                                 to='candidate.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='person',
            name='conflict_resolved',
        ),
        migrations.AddField(
            model_name='person',
            name='caveats_timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
