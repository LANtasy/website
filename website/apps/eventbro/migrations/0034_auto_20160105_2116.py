# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0033_auto_20160105_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='convention',
            field=models.ForeignKey(related_name='event_convention_uid', to='eventbro.Convention'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='convention',
            field=models.ForeignKey(related_name='sponsor_convention_uid', to='eventbro.Convention'),
        ),
    ]
