from __future__ import unicode_literals, absolute_import

import logging
# from decimal import Decimal
from cartridge.shop.models import Product, ProductVariation

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

    def get_full_name(self):
        return self.__unicode__()

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

    def upgradeable_to(self):
        options = TicketOption.objects.all()
        current_price = self.price()
        option_ids = [option.id for option in options if option.price() >= current_price]
        return TicketOption.objects.filter(id__in=option_ids).exclude(id=self.id)

    def has_stock(self, quantity=1):
        variations = ProductVariation.objects.filter(product=self)
        for variation in variations:
            if variation.has_stock(quantity):
                return True

        return False


class Ticket(Product):

    @models.permalink
    def get_absolute_url(self):
        return ("salesbro:ticket_detail", (), {"slug": self.slug})

    def has_stock(self, quantity=1):
        ticket_options = TicketOption.objects.filter(ticket=self)

        for ticket_option in ticket_options:
            if ticket_option.has_stock(quantity):
                return True

        return False
