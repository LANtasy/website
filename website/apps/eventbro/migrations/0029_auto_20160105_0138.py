# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0028_auto_20160105_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='id',
        ),
        migrations.RemoveField(
            model_name='event',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='id',
        ),
        migrations.AlterField(
            model_name='convention',
            name='uid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='uid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='uid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True),
        ),
    ]
