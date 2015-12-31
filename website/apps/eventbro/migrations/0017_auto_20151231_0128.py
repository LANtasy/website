# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0016_event_sponsor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
