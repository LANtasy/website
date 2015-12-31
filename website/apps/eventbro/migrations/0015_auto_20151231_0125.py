# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import website.apps.eventbro.models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0014_auto_20151229_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Group Name', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', sorl.thumbnail.fields.ImageField(null=True, upload_to=website.apps.eventbro.models.rename_image, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='prizes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='rules',
            field=models.TextField(null=True, blank=True),
        ),
    ]
