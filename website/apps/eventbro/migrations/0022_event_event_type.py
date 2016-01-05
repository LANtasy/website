# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0021_auto_20160104_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(related_name='event_type_id', blank=True, to='eventbro.EventType', null=True),
        ),
    ]
