# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0019_auto_20160101_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(max_length=3, choices=[('LAN', 'BYOC LAN'), ('MIN', 'Miniatures'), ('RPG', 'RPG'), ('TAB', 'Tabletop'), ('BDG', 'Board Game')]),
        ),
    ]
