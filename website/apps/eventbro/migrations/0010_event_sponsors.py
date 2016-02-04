# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0009_auto_20160115_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sponsors',
            field=models.ManyToManyField(related_name='event_sponsors', to='eventbro.Sponsor', blank=True),
        ),
    ]
