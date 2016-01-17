# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='event',
            field=models.ForeignKey(related_name='registrants', blank=True, to='eventbro.Event', null=True),
        ),
    ]
