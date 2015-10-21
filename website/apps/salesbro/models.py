from __future__ import unicode_literals, absolute_import

import logging
# from decimal import Decimal
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
    def get_price_difference(self):
        if self.has_price():
            unit_price = (self.unit_price - self.ticket.unit_price)
            if self.on_sale():
                sale_price = (self.sale_price - self.ticket.unit_price)
                if sale_price < 0 and unit_price < 0:
                    return '-${sale_price}'.format(sale_price=-sale_price)
                elif sale_price < 0:
                    return '-${sale_price}'.format(sale_price=-sale_price)
                elif sale_price == 0:
                    return '+$0.00'
                else:
                    return '+${sale_price}'.format(sale_price=sale_price)
            else:
                return '+${unit_price}'.format(unit_price=unit_price)
        else:
            return '+$0.00'

    @models.permalink
    def get_absolute_url(self):
        return ("salesbro:ticket_detail", (), {"slug": self.ticket.slug})


class Ticket(Product):

    @models.permalink
    def get_absolute_url(self):
        return ("salesbro:ticket_detail", (), {"slug": self.slug})
