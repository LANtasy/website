# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0011_auto_20151214_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(height_field=100, null=True, upload_to=b'eventbro/events', blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='group_captain',
            field=models.BooleanField(default=False),
        ),
    ]
