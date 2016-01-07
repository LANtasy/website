# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


group_name = 'Event editor'
permissions = ['add_event', 'change_event', 'delete_event']


def add_event_editor(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        group = Group(name=group_name)
        group.save()

    for permission_name in permissions:
        try:
            permission = Permission.objects.get(codename=permission_name)
            group.permissions.add(permission)
        except Permission.DoesNotExist, e:
            raise e
        except Group.DoesNotExist, e:
            raise e


def remove_event_editor(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    try:
        group_object = Group.objects.get(name=group_name)
        group_object.delete()
    except Group.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0002_auto_20160106_0031'),
    ]

    operations = [
        migrations.RunPython(add_event_editor, remove_event_editor),
    ]
