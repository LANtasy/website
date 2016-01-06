# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0020_auto_20160101_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('overlapping', models.BooleanField(default=False, verbose_name=b'Overlapping event registration')),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_type',
        ),
    ]
