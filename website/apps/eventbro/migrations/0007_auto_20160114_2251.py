# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0006_event_showcase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='showcase',
        ),
        migrations.AddField(
            model_name='event',
            name='disable_registration',
            field=models.BooleanField(default=False, verbose_name=b'Disable Event Registration'),
        ),
    ]
