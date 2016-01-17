# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0008_convention_allow_registration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convention',
            name='allow_registration',
        ),
        migrations.AddField(
            model_name='convention',
            name='registration',
            field=models.BooleanField(default=False, verbose_name=b'Registration'),
        ),
    ]
