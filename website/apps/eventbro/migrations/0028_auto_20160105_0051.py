# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


model_types = ['Convention', 'Sponsor', 'Event']


def generate_uuids(apps, schema_editor):
    for model_type in model_types:
        Model = apps.get_model('eventbro', model_type)
        model_objects = Model.objects.all()
        for model_object in model_objects:
            model_object.uid = uuid.uuid4()
            model_object.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0027_auto_20160105_0124'),
    ]

    operations = [
        migrations.RunPython(generate_uuids, do_nothing),
    ]
