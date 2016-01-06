# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0028_auto_20160105_1819'),
    ]

    operations = [
        # Step 2 - Add placeholder fields
        migrations.AddField(
            model_name='sponsor',
            name='tmp',
            field=models.ForeignKey(related_name='sponsor_convention_uid', to='eventbro.Convention', blank=True,
                                    null=True, to_field='uid'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='tmp',
            field=models.ForeignKey(related_name='event_convention_uid', to='eventbro.Convention', blank=True,
                                    null=True, to_field='uid'),
            preserve_default=False,
        ),
    ]
