# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0036_auto_20160105_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsor',
            name='id',
        ),
        migrations.AlterField(
            model_name='event',
            name='sponsor',
            field=models.ForeignKey(related_name='event_sponsor', blank=True, to='eventbro.Sponsor', null=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='uid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True),
        ),
    ]
