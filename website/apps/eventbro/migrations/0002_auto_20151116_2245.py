# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='convention',
            name='start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(verbose_name=b'End Time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(verbose_name=b'Start Time'),
        ),
    ]
