# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0012_remove_event_sponsor'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='subname',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Event Subname', blank=True),
        ),
    ]
