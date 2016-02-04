# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def make_many_sponsors(apps, schema_editor):
    Event = apps.get_model('eventbro', 'Event')

    for event in Event.objects.all():
        event.sponsors.add(event.sponsor)


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0010_event_sponsors'),
    ]

    operations = [
        migrations.RunPython(make_many_sponsors),
    ]
