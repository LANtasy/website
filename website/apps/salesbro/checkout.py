from __future__ import unicode_literals, absolute_import

import logging
from django.db import transaction
from website.apps.badgebro.models import Badge
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


def salesbro_order_handler(request, order_form, order):
    """
    Finds all passes due to purchased ticket options
    Creates all passes with associated types
    Relate all passes to original order
    Make passes available for registration/assignment
    """
    with transaction.atomic():

        for item in order.items.all():
            ticket_option = TicketOption.objects.get(sku=item.sku)
            for x in range(0, item.quantity):

                badge = Badge()
                badge.order = order
                badge.ticket = ticket_option
                badge.save()

        order.status = 2
        order.save()
