# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'attachments/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('state', models.IntegerField(default=0, choices=[(0, b'NULL'), (1, b'Rejected'), (2, b'First message'), (3, b'No response'), (4, b'Negative response'), (5, b'Positive response'), (6, b'1s'), (7, b'Resigned'), (8, b'>1'), (9, b'Rejected after meeting'), (10, b'Hired')])),
                ('caveats', models.TextField(max_length=1000, blank=True)),
                ('comm', models.ForeignKey(to='candidate.Communication')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linkedin', models.URLField(unique=True, null=True)),
                ('goldenline', models.URLField(unique=True, null=True)),
                ('email', models.EmailField(max_length=75, unique=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='role',
            field=models.ForeignKey(blank=True, to='candidate.Role', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='source',
            field=models.ForeignKey(to='candidate.Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='person',
            field=models.ForeignKey(default=1, to='candidate.Person'),
            preserve_default=True,
        ),
    ]
