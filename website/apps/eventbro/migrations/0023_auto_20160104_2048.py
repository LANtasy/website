# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


event_types = [
        {
            'short': 'LAN',
            'uid': 'b5a958c1-1ef5-494d-b1cd-8e1b1a77698d',
            'name': 'LAN games',
            'overlapping': True,
        },
        {
            'short': 'MIN',
            'uid': '14a091e3-d9cd-482c-bbef-639577ab3aab',
            'name': 'Miniatures',
            'overlapping': False,
        },
        {
            'short': 'RPG',
            'uid': 'c1e3a5d2-2b97-48bf-ba77-4f0f909fedd7',
            'name': 'RPGs',
            'overlapping': False,
        },
        {
            'short': 'TAB',
            'uid': '9dd54c22-e70f-4546-852c-017d365b40f0',
            'name': 'Tabletop games',
            'overlapping': False,
        },
        {
            'short': 'BDG',
            'uid': '6e58290b-8a5b-441c-8c61-f480468967cb',
            'name': 'Board games',
            'overlapping': False,
        },
]


def add_event_types(apps, schema_editor):
    EventType = apps.get_model('eventbro', 'EventType')
    for event_type in event_types:
        try:
            EventType.objects.get(uid=event_type.get('uid'))
        except EventType.DoesNotExist:
            event_type_object = EventType.objects.create(uid=event_type.get('uid'), name=event_type.get('name'),
                                                         overlapping=event_type.get('overlapping'))
            event_type_object.save()


def remove_event_types(apps, schema_editor):
    EventType = apps.get_model('eventbro', 'EventType')
    for event_type in event_types:
        try:
            event_type_object = EventType.objects.get(uid=event_type.get('uid'))
            event_type_object.delete()
        except EventType.DoesNotExist:
            pass




class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0022_event_event_type'),
    ]

    operations = [
        migrations.RunPython(add_event_types, remove_event_types),
    ]
