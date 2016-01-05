# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0025_auto_20160105_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
    ]
