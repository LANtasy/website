# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0013_auto_20160218_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='option',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='badge',
            name='type',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='network',
            field=models.CharField(default=b'general', max_length=20, choices=[(b'vendor', b'Vendor'), (b'tournament', b'Tournament'), (b'staff', b'Staff'), (b'general', b'General')]),
        ),
    ]
