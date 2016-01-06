# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from itertools import chain


def migrate_forward(apps, schema_editor):
    convention = apps.get_model('eventbro', 'Convention')
    sponsor = apps.get_model('eventbro', 'Sponsor')
    sponsors = sponsor.objects.all()
    for sponsor in sponsors:
        try:
            uid = sponsor.convention.uid
            sponsor.tmp = convention.objects.get(uid=uid)
            sponsor.save()
        except:
            print 'exception detected'
            pass

    event = apps.get_model('eventbro', 'Event')
    events = event.objects.all()
    for event in events:
        try:
            uid = event.convention.uid
            event.tmp = convention.objects.get(uid=uid)
            event.save()
        except:
            print 'exception detected'
            pass


def migrate_backward(apps, schema_editor):
    convention = apps.get_model('eventbro', 'Convention')
    sponsor = apps.get_model('eventbro', 'Sponsor')
    sponsors = sponsor.objects.all()
    for sponsor in sponsors:
        try:
            fk_id = sponsor.tmp.id
            sponsor.convention = convention.objects.get(id=fk_id)
            sponsor.save()
        except:
            print 'exception detected'
            pass

    event = apps.get_model('eventbro', 'Event')
    events = event.objects.all()
    for event in events:
        try:
            fk_id = event.tmp.id
            event.convention = convention.objects.get(id=fk_id)
            event.save()
        except:
            print 'exception detected'
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0029_auto_20160105_1855'),
    ]

    operations = [
        # Step 3 - Migrate
        migrations.RunPython(migrate_forward, migrate_backward)
    ]
