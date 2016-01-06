# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0010_auto_20151214_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=3, null=True, choices=[('LAN', 'BYOC LAN'), ('MIN', 'Miniatures'), ('TAB', 'Tabletop'), ('RPG', 'RPG')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='valid_options',
            field=models.ManyToManyField(related_name='event_valid_tickets', verbose_name=b'Valid participants', to='salesbro.TicketOption'),
        ),
    ]
