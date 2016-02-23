# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0011_auto_20160213_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='qr_code',
            field=models.ImageField(null=True, upload_to=b'badges/qrcodes/%Y', blank=True),
        ),
        migrations.AlterField(
            model_name='badge',
            name='type',
            field=models.CharField(default=b'general', max_length=20, verbose_name=b'Customer Type', choices=[(b'vendor', b'Vendor'), (b'tournament', b'Tournament'), (b'staff', b'Staff'), (b'general', b'General')]),
        ),
    ]
