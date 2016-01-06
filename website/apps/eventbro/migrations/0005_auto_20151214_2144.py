# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0004_convention_available'),
    ]

    operations = [
        migrations.RenameField(
            model_name='convention',
            old_name='available',
            new_name='published',
        ),
        migrations.AddField(
            model_name='event',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
