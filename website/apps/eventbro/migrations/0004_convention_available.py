# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0003_auto_20151116_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
