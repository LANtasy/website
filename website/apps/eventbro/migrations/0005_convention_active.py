# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0004_sponsor_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
