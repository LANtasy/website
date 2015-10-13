# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150527_1127'),
        ('badgebro', '0004_auto_20150919_0738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badge',
            name='order_item',
        ),
        migrations.AddField(
            model_name='badge',
            name='order',
            field=models.ForeignKey(related_name='badge_order_id', default=1, to='shop.Order'),
            preserve_default=False,
        ),
    ]
