# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def null_existing_event(apps, schema_editor):
    Event = apps.get_model('eventbro', 'Event')
    existing_events = Event.objects.all()
    for existing_event in existing_events:
        existing_event.event_type = None
        existing_event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0020_auto_20160101_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('overlapping', models.BooleanField(default=False, verbose_name=b'Overlapping event registration')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=3, null=True, choices=[('LAN', 'BYOC LAN'), ('MIN', 'Miniatures'), ('RPG', 'RPG'), ('TAB', 'Tabletop'), ('BDG', 'Board Game')]),
        ),
        migrations.RunPython(null_existing_event, null_existing_event),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(related_name='event_type_id', blank=True, to='eventbro.EventType', null=True),
        ),
    ]
