# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0006_badge_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='type',
            field=models.CharField(default=b'general', max_length=20, choices=[(b'vendor', b'Vendor'), (b'tournament', b'Tournament'), (b'staff', b'Staff'), (b'general', b'General')]),
        ),
    ]
