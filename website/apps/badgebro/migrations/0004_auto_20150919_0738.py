# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0003_auto_20150919_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='badge',
            name='order_item',
            field=models.OneToOneField(to='shop.OrderItem'),
        ),
    ]
