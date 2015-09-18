# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150527_1127'),
        ('salesbro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketOption',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shop.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=('shop.product',),
        ),
        migrations.AddField(
            model_name='ticket',
            name='option',
            field=models.ForeignKey(blank=True, to='salesbro.TicketOption', null=True),
        ),
    ]
