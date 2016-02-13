# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badgebro', '0008_auto_20160111_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='qr_code',
            field=models.ImageField(null=True, upload_to=b'badges/qrcodes/%Y', blank=True),
        ),
    ]
