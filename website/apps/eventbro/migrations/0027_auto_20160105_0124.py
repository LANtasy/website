# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import autoslug
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0026_auto_20160105_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='name',
            field=models.CharField(default='change-me', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
    ]
