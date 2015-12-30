# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations, models

group_name = 'Event editor'
permissions = ['add_event', 'change_event', 'delete_event']


def add_event_editor(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    try:
        group = Group.objects.get(name=group_name)
    except ObjectDoesNotExist:
        group = Group(name=group_name)
        group.save()

    for permission_name in permissions:
        try:
            permission = Permission.objects.get(codename=permission_name)
            group.permissions.add(permission)
        except Permission.DoesNotExist, e:
            raise e


def remove_event_editor(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    try:
        group_object = Group.objects.get(name=group_name)
        group_object.delete()
    except ObjectDoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0013_auto_20151229_2315'),
    ]

    operations = [
        migrations.RunPython(add_event_editor, remove_event_editor),
    ]
