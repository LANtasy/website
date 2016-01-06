# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0032_auto_20160105_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='id',
        ),
        migrations.AlterField(
            model_name='convention',
            name='uid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='convention',
            field=models.ForeignKey(related_name='event_convention_uid', blank=True, to='eventbro.Convention', null=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='convention',
            field=models.ForeignKey(related_name='sponsor_convention_uid', blank=True, to='eventbro.Convention', null=True),
        ),
    ]
