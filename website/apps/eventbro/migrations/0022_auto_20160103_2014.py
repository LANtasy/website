# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


event_types = [
        {
            'short': 'LAN',
            'name': 'LAN games',
            'overlapping': True,
        },
        {
            'short': 'MIN',
            'name': 'Miniatures',
            'overlapping': False,
        },
        {
            'short': 'RPG',
            'name': 'RPGs',
            'overlapping': False,
        },
        {
            'short': 'TAB',
            'name': 'Tabletop games',
            'overlapping': False,
        },
        {
            'short': 'BDG',
            'name': 'Board games',
            'overlapping': False,
        },
]


def add_event_types(apps, schema_editor):
    EventType = apps.get_model('eventbro', 'EventType')
    for event_type in event_types:
        try:
            EventType.objects.get(name=event_type.get('name'))
        except EventType.DoesNotExist:
            event_type_object = EventType.objects.create(name=event_type.get('name'),
                                                         overlapping=event_type.get('overlapping'))
            event_type_object.save()


def remove_event_types(apps, schema_editor):
    EventType = apps.get_model('eventbro', 'EventType')
    for event_type in event_types:
        try:
            event_type_object = EventType.objects.get(name=event_type.get('name'))
            event_type_object.delete()
        except EventType.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0021_auto_20160104_0201'),
    ]

    operations = [
        migrations.RunPython(add_event_types, remove_event_types),
    ]
