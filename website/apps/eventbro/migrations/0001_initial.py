# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('start', models.DateTimeField(auto_now=True)),
                ('end', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Event Name')),
                ('description', models.TextField()),
                ('start', models.DateTimeField(auto_now=True, verbose_name=b'Start Time')),
                ('end', models.DateTimeField(auto_now=True, verbose_name=b'End Time')),
                ('size', models.PositiveSmallIntegerField(verbose_name=b'Max Size')),
                ('convention', models.ForeignKey(related_name='event_convention_id', to='eventbro.Convention')),
            ],
        ),
    ]
