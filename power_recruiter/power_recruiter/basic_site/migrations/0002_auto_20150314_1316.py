# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='edge',
            name='state_in',
            field=models.ForeignKey(related_name=b's_in', to='basic_site.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edge',
            name='state_out',
            field=models.ForeignKey(related_name=b's_out', to='basic_site.State'),
            preserve_default=True,
        ),
    ]
