# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0037_auto_20160105_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='event',
        ),
    ]
