# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150527_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=('shop.product',),
        ),
    ]
