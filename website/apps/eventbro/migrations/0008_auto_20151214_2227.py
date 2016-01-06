# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0005_auto_20151024_1544'),
        ('eventbro', '0007_event_valid_tickets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='valid_tickets',
        ),
        migrations.AddField(
            model_name='event',
            name='valid_options',
            field=models.ManyToManyField(related_name='event_valid_tickets', to='salesbro.TicketOption'),
        ),
    ]
