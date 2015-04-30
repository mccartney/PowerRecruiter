# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('basic_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'attachments/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OldState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('start_date',
                 models.DateTimeField(default=django.utils.timezone.now)),
                ('change_date',
                 models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('current_state_started',
                 models.DateTimeField(default=django.utils.timezone.now)),
                ('photo_url', models.CharField(max_length=200)),
                ('linkedin', models.URLField(unique=True, null=True)),
                ('goldenline', models.URLField(unique=True, null=True)),
                ('email',
                 models.EmailField(max_length=75, unique=True, null=True)),
                ('caveats', models.TextField(max_length=1000, blank=True)),
                ('conflict_resolved', models.BooleanField(default=False)),
                ('state', models.ForeignKey(to='basic_site.State', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='oldstate',
            name='person',
            field=models.ForeignKey(to='candidate.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oldstate',
            name='state',
            field=models.ForeignKey(to='basic_site.State', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='person',
            field=models.ForeignKey(to='candidate.Person'),
            preserve_default=True,
        ),
    ]
