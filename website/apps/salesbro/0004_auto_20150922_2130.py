# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime


def add_link(apps, schema_editor):
    link = apps.get_model('pages', 'Link')
    link_object = link(id=1,
                       content_model=u'link',
                       description=u'Tickets',
                       title=u'Tickets',
                       titles=u'Tickets',
                       slug=u'tickets/',
                       status=1,
                       site_id=1)
    link_object.save()

def remove_link(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0003_auto_20150908_0416'),
    ]

    operations = [
        migrations.RunPython(add_link, remove_link),
    ]
