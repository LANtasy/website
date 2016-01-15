# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist

link_name = u'Tickets'


def add_ticket_link(apps, schema_editor):
    link = apps.get_model('pages', 'Link')
    try:
        link.objects.get(title=link_name)
    except ObjectDoesNotExist:
        new_object = link(title=link_name,
                          titles=link_name,
                          description=link_name,
                          content_model=u'link',
                          slug=u'tickets/',
                          status=1,
                          site_id=1)
        new_object.save()


def remove_ticket_link(apps, schema_editor):
    link = apps.get_model('pages', 'Link')
    try:
        old_object = link.objects.get(title=link_name)
        old_object.delete()
    except ObjectDoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0004_auto_20150922_2130'),
    ]

    operations = [
        # migrations.RunPython(add_ticket_link, remove_ticket_link),
    ]
