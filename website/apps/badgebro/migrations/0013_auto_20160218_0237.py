# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0012_auto_20160215_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='badge',
            old_name='type',
            new_name='network',
        ),
    ]
