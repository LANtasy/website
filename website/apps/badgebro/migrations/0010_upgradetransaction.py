# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0005_auto_20151024_1544'),
        ('badgebro', '0009_auto_20160212_2045'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpgradeTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_method', models.CharField(max_length=10, choices=[(b'visa', b'Visa'), (b'mastercard', b'Mastercard'), (b'discover', b'Discover'), (b'amex', b'American Express'), (b'debit', b'Debit'), (b'cash', b'Cash')])),
                ('difference', models.DecimalField(max_digits=10, decimal_places=2)),
                ('tax', models.DecimalField(max_digits=10, decimal_places=2)),
                ('total', models.DecimalField(max_digits=10, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('badge', models.ForeignKey(related_name='upgrades', to='badgebro.Badge')),
                ('new_ticket', models.ForeignKey(related_name='+', to='salesbro.TicketOption')),
                ('old_ticket', models.ForeignKey(related_name='+', to='salesbro.TicketOption')),
            ],
        ),
    ]
