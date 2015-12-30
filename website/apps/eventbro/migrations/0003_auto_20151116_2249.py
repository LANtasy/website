# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0002_auto_20151116_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
