# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0009_auto_20151214_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=3, null=True, choices=[('LAN', 'BYOC LAN'), ('MIN', 'Miniatures'), ('TAB', 'Tabletop')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='game_id_name',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Unique identifier', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='group_event',
            field=models.BooleanField(default=False, verbose_name=b'Is group event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='require_game_id',
            field=models.BooleanField(default=False, verbose_name=b'Require special ID'),
        ),
        migrations.AlterField(
            model_name='event',
            name='valid_options',
            field=models.ManyToManyField(related_name='event_valid_tickets', verbose_name=b'Tickets that can participate in this event', to='salesbro.TicketOption'),
        ),
    ]
