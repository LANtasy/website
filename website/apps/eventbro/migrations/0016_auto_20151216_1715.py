# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import website.apps.eventbro.models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0015_auto_20151216_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='thumbnail',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=website.apps.eventbro.models.rename_image, blank=True),
        ),
    ]
