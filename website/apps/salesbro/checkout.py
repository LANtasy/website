from __future__ import unicode_literals, absolute_import
from decimal import Decimal

import logging
from cartridge.shop.utils import set_tax
from cartridge.shop.models import DiscountCode
from django.db import transaction
import math
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
                Badge.objects.create_badge(order=order, item=item, ticket_option=ticket_option)
        # Testing a thing
        asdf = None
        order.status = 2
        order.save()


def salesbro_tax_handler(request, order_form):
    """
    Default tax handler - called immediately after the handler defined
    by ``SHOP_HANDLER_BILLING_SHIPPING``. Implement your own and
    specify the path to import it from via the setting
    ``SHOP_HANDLER_TAX``. This function will typically contain any tax
    calculation where the tax amount can then be set using the function
    ``cartridge.shop.utils.set_tax``. The Cart object is also
    accessible via ``request.cart``
    """
    total = request.cart.total_price()

    # To implement PST would need to do the following
    # - Keep track of GST total_price (all things)
    # - Keep track fo PST total_price (no Ticket or TicketOptions)
    # - Need a new calculation for discount
    # - Change gst and pst calculation

    if 'discount_code' in request.session:
        discount_code = DiscountCode.objects.get(code=request.session['discount_code'])
        discount = request.cart.calculate_discount(discount_code)
        total -= discount

    # pst = total * Decimal(0.07)
    gst = total * Decimal(0.05)

    # tax = math.ceil(pst*100 + gst*100)/100
    tax = math.ceil(gst*100)/100

    set_tax(request, "GST", tax)

