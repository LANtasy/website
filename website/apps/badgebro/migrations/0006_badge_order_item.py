# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150527_1127'),
        ('badgebro', '0005_auto_20151008_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='order_item',
            field=models.ForeignKey(related_name='badge_order_item', default=1, to='shop.OrderItem'),
            preserve_default=False,
        ),
    ]
