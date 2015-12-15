# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0008_auto_20151214_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='added',
            new_name='date_added',
        ),
        migrations.AddField(
            model_name='event',
            name='game_id_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='group_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='require_game_id',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registration',
            name='game_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='registration',
            name='group_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='size',
            field=models.PositiveSmallIntegerField(null=True, verbose_name=b'Max Size', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='valid_options',
            field=models.ManyToManyField(related_name='event_valid_tickets', null=True, to='salesbro.TicketOption', blank=True),
        ),
    ]
