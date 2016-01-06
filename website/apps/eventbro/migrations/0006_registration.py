# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventbro', '0005_auto_20151214_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(related_name='registration_event', to='eventbro.Event')),
                ('user', models.ForeignKey(related_name='registration_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
