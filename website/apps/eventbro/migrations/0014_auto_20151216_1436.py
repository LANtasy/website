# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0013_auto_20151216_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='image',
        ),
        migrations.AddField(
            model_name='event',
            name='thumbnail',
            field=models.ImageField(max_length=32, null=True, upload_to=b'eventbro/events', blank=True),
        ),
        migrations.DeleteModel(
            name='EventImages',
        ),
    ]
