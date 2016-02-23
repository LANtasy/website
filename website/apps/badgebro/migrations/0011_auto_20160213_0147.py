# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0010_upgradetransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upgradetransaction',
            name='difference',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='upgradetransaction',
            name='tax',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='upgradetransaction',
            name='total',
            field=models.IntegerField(),
        ),
    ]
