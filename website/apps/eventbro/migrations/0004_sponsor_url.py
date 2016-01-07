# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0003_auto_20160106_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='url',
            field=models.URLField(max_length=255, null=True, blank=True),
        ),
    ]
