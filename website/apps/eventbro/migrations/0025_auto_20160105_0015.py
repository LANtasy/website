# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from autoslug.utils import slugify
from django.db import migrations, models


model_types = ['Convention', 'Sponsor', 'EventType', 'Event']


def modify_slugs(apps, schema_editor):
    for model_type in model_types:
        Model = apps.get_model('eventbro', model_type)
        model_objects = Model.objects.all()
        for model_object in model_objects:
            name = model_object.name
            model_object.slug = slugify(name)
            model_object.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0024_auto_20160105_0014'),
    ]

    operations = [
        migrations.RunPython(modify_slugs, do_nothing),
    ]
