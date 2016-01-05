# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0023_auto_20160104_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='eventtype',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'name', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='uid',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True),
        ),
    ]
