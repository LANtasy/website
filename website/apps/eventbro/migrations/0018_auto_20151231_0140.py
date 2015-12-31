# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventbro', '0017_auto_20151231_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='convention',
            field=models.ForeignKey(related_name='sponsor_convention', default=0, to='eventbro.Convention'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Presenting'), (2, b'Gold'), (3, b'Silver'), (4, b'Bronze')]),
        ),
    ]
