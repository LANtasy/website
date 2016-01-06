# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0031_auto_20160105_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='tmp',
            new_name='convention',
        ),
        migrations.RenameField(
            model_name='sponsor',
            old_name='tmp',
            new_name='convention',
        ),
    ]
