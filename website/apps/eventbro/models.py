import uuid

import os
from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from website.apps.salesbro.models import Ticket, TicketOption
from sorl.thumbnail import ImageField


class Convention(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return '{name}'.format(name=self.name)


def rename_image(instance, filename):
    extension = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), extension)
    return os.path.join('eventbro/images', filename)


class Event(models.Model):
    BYOC_LAN = u'LAN'
    MINIATURES = u'MIN'
    TABLETOP = u'TAB'
    RPG = u'RPG'
    EVENT_TYPE_CHOICES = (
        (BYOC_LAN, u'BYOC LAN'),
        (MINIATURES, u'Miniatures'),
        (TABLETOP, u'Tabletop'),
        (RPG, u'RPG'),
    )

    convention = models.ForeignKey(Convention, related_name='event_convention_id')
    name = models.CharField(verbose_name='Event Name', max_length=100)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField(verbose_name='Start Time')
    end = models.DateTimeField(verbose_name='End Time')
    size = models.PositiveSmallIntegerField(verbose_name='Max Size', blank=True, null=True)
    published = models.BooleanField(default=False)
    valid_options = models.ManyToManyField(TicketOption, related_name='event_valid_tickets',
                                           verbose_name='Valid participants')
    group_event = models.BooleanField(default=False, verbose_name='Is group event')
    require_game_id = models.BooleanField(default=False, verbose_name='Require special ID')
    game_id_name = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name='Unique identifier')
    event_type = models.CharField(max_length=3, choices=EVENT_TYPE_CHOICES, blank=True, null=True)
    image = ImageField(upload_to=rename_image, blank=True, null=True)

    def available_spots(self):
        registered = Registration.objects.filter(event=self).count()
        available = self.size - registered
        return available
    # annotate count


class Registration(models.Model):
    user = models.ForeignKey(User, related_name='registration_user')
    event = models.ForeignKey(Event, related_name='registration_event')
    date_added = models.DateTimeField(auto_now_add=True)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    group_captain = models.BooleanField(default=False)
    game_id = models.CharField(max_length=255, blank=True, null=True)

