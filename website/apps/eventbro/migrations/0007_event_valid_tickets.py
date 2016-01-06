# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0005_auto_20151024_1544'),
        ('eventbro', '0006_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='valid_tickets',
            field=models.ManyToManyField(related_name='event_valid_tickets', to='salesbro.Ticket'),
        ),
    ]
