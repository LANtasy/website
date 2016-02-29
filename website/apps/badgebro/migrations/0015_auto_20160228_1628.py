# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0014_auto_20160220_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='first_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='last_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
