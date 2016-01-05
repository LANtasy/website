# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0029_auto_20160105_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False),
        ),
    ]
