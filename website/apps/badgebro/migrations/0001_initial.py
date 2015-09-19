# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20150527_1127'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salesbro', '0003_auto_20150908_0416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(max_length=34)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(related_name='badges', to='shop.Order')),
                ('ticket', models.ForeignKey(related_name='badges', to='salesbro.TicketOption')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
