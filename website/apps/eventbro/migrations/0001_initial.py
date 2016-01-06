# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import website.apps.eventbro.models
import autoslug.fields
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salesbro', '0005_auto_20151024_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Convention',
            fields=[
                ('uid', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Event Name')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('start', models.DateTimeField(verbose_name=b'Start Time')),
                ('end', models.DateTimeField(verbose_name=b'End Time')),
                ('size', models.PositiveSmallIntegerField(null=True, verbose_name=b'Max Size', blank=True)),
                ('published', models.BooleanField(default=False)),
                ('group_event', models.BooleanField(default=False, verbose_name=b'Is group event')),
                ('require_game_id', models.BooleanField(default=False, verbose_name=b'Require special ID')),
                ('game_id_name', models.CharField(max_length=100, null=True, verbose_name=b'Unique identifier', blank=True)),
                ('image', sorl.thumbnail.fields.ImageField(null=True, upload_to=website.apps.eventbro.models.rename_image, blank=True)),
                ('prizes', models.TextField(null=True, blank=True)),
                ('rules', models.TextField(null=True, blank=True)),
                ('organizer', models.CharField(max_length=100, null=True, blank=True)),
                ('convention', models.ForeignKey(related_name='event_convention_uid', to='eventbro.Convention')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('uid', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('overlapping', models.BooleanField(default=False, verbose_name=b'Overlapping event registration')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('group_name', models.CharField(max_length=255, null=True, verbose_name=b'Group Name', blank=True)),
                ('group_captain', models.BooleanField(default=False)),
                ('game_id', models.CharField(help_text=b'eg Battle.net ID, Summoner ID, etc', max_length=255, null=True, verbose_name=b'Game ID', blank=True)),
                ('event', models.ForeignKey(related_name='registrats', blank=True, to='eventbro.Event', null=True)),
                ('user', models.ForeignKey(related_name='registration_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('uid', models.UUIDField(primary_key=True, default=uuid.uuid4, serialize=False, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', unique=True, editable=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', sorl.thumbnail.fields.ImageField(null=True, upload_to=website.apps.eventbro.models.rename_image, blank=True)),
                ('level', models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, b'Presenting'), (2, b'Gold'), (3, b'Silver'), (4, b'Bronze')])),
                ('convention', models.ForeignKey(related_name='sponsor_convention_uid', to='eventbro.Convention')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(related_name='event_type_id', blank=True, to='eventbro.EventType', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='sponsor',
            field=models.ForeignKey(related_name='event_sponsor', blank=True, to='eventbro.Sponsor', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='valid_options',
            field=models.ManyToManyField(related_name='event_valid_tickets', verbose_name=b'Valid participants', to='salesbro.TicketOption'),
        ),
    ]
