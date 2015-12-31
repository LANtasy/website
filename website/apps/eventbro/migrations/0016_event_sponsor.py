# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0015_auto_20151231_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sponsor',
            field=models.ForeignKey(related_name='event_sponsor', blank=True, to='eventbro.Sponsor', null=True),
        ),
    ]
