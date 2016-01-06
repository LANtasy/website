# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0030_auto_20160105_1856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='convention',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='convention',
        ),
    ]
