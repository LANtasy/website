# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_none(apps, schema_editor):
    event_model = apps.get_model('eventbro', 'Event')
    events = event_model.objects.all()
    for event in events:
        event.sponsor = None
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0035_sponsor_uid'),
    ]

    operations = [
        migrations.RunPython(set_none, set_none),
        migrations.AlterField(
            model_name='event',
            name='sponsor',
            field=models.ForeignKey(related_name='event_sponsor', to_field=b'uid', blank=True, to='eventbro.Sponsor', null=True),
        ),
        migrations.RunPython(set_none, set_none),
    ]
