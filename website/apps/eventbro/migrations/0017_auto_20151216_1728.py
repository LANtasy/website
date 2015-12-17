# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0016_auto_20151216_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='thumbnail',
            new_name='image',
        ),
    ]
