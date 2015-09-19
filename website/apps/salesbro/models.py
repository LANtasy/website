from __future__ import unicode_literals, absolute_import

import logging
from cartridge.shop.models import Product

from django.db import models
from mezzanine.core.managers import DisplayableManager

logger = logging.getLogger(__name__)


class TicketOptionManager(DisplayableManager):
    def available(self):
        qs = self.get_queryset()
        qs = qs.filter(available=True)

        return qs


class TicketOption(Product):
    objects = TicketOptionManager()
    ticket = models.ForeignKey('Ticket')

    def __unicode__(self):
        return '{title} ({ticket})'.format(title=self.title, ticket=self.ticket.title)

    @property
    def pricediff(self):
        return self.price() - self.ticket.price()


class Ticket(Product):

    @models.permalink
    def get_absolute_url(self):
        return ("salesbro:ticket_detail", (), {"slug": self.slug})
