# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0007_badge_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='first_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='badge',
            name='last_name',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='order',
            field=models.ForeignKey(related_name='badge_order_id', blank=True, to='shop.Order', null=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='order_item',
            field=models.ForeignKey(related_name='badge_order_item', blank=True, to='shop.OrderItem', null=True),
        ),
    ]
