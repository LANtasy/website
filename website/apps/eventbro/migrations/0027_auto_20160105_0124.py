# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0026_auto_20160105_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='name',
            field=models.CharField(default='change-me', max_length=255),
            preserve_default=False,
        ),
    ]
