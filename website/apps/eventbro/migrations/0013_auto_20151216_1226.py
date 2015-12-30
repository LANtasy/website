# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0012_auto_20151216_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'eventbro/events', blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'eventbro/events/thumbs', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ForeignKey(related_name='event_image', blank=True, to='eventbro.EventImages', null=True),
        ),
    ]
