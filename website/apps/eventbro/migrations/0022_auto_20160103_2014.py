# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0021_auto_20160104_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(related_name='event_type_id', blank=True, to='eventbro.EventType', null=True),
        ),
    ]
