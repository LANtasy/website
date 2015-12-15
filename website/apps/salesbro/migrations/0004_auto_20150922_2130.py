# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist

group_name = u'Sales Portal Access'


def add_ticket_sales(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    try:
        group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        new_group = group(name=group_name)
        new_group.save()


def remove_ticket_sales(apps, schema_editor):
    group = apps.get_model('auth', 'Group')
    try:
        group_object = group.objects.get(name=group_name)
        group_object.delete()
    except ObjectDoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0003_auto_20150908_0416'),
    ]

    operations = [
        migrations.RunPython(add_ticket_sales, remove_ticket_sales),
    ]
