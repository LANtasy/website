# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0034_auto_20160105_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
