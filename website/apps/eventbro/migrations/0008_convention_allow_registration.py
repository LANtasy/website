# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0007_auto_20160114_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='allow_registration',
            field=models.BooleanField(default=False),
        ),
    ]
