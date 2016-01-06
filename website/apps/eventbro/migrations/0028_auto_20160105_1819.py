# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('eventbro', '0027_auto_20160105_0124'),
    ]

    operations = [
        # Step 1 - Create field
        migrations.AddField(
            model_name='convention',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
