from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import Group, Permission

from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.add_event_editor()

    def add_event_editor(self):
        group_permissions = [
            {
                'name': 'Event editor',
                'permissions': ['add_event', 'change_event']
            },
            {
                'name': 'Event admin',
                'permissions': ['add_event', 'change_event', 'delete_event', 'delete_registration']
            },
            {
                'name': 'Registration editor',
                'permissions': ['add_registration', 'change_registration']
            },
        ]

        for group_permission in group_permissions:
            try:
                group = Group.objects.get(name=group_permission.get('name'))
            except Group.DoesNotExist:
                group = Group(name=group_permission.get('name'))
                group.save()

            for permission_name in group_permission.get('permissions'):
                try:
                    permission = Permission.objects.get(codename=permission_name)
                    group.permissions.add(permission)
                except Permission.DoesNotExist, e:
                    raise e
                except Group.DoesNotExist, e:
                    raise e


