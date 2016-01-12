# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0005_convention_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='showcase',
            field=models.BooleanField(default=False, verbose_name=b'Showcase event'),
        ),
    ]
