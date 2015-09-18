# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salesbro', '0002_auto_20150908_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='option',
        ),
        migrations.AddField(
            model_name='ticketoption',
            name='ticket',
            field=models.ForeignKey(default=3, to='salesbro.Ticket'),
            preserve_default=False,
        ),
    ]
