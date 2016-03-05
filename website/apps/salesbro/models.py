from __future__ import unicode_literals, absolute_import

import logging
# from decimal import Decimal
from cartridge.shop import fields
from cartridge.shop.models import Product, SelectedProduct, ProductVariation, DiscountCode
from decimal import Decimal

from cartridge.shop.utils import clear_session
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.managers import DisplayableManager, CurrentSiteManager

from website.apps.badgebro.models import Badge

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


class Ticket(Product):

    @models.permalink
    def get_absolute_url(self):
        return ("salesbro:ticket_detail", (), {"slug": self.slug})


class TransactionManager(CurrentSiteManager):

    def from_request(self, request):
        """
        Returns the last order made by session key. Used for
        Google Anayltics order tracking in the order complete view,
        and in tests.
        """
        orders = self.filter(key=request.session.session_key).order_by("-id")
        if orders:
            return orders[0]
        raise self.model.DoesNotExist

    def get_for_user(self, order_id, request):
        """
        Used for retrieving a single order, ensuring the user in
        the given request object can access it.
        """
        lookup = {"id": order_id}
        if not request.user.is_authenticated():
            lookup["key"] = request.session.session_key
        elif not request.user.is_staff:
            lookup["user_id"] = request.user.id
        return self.get(**lookup)


class Transaction(models.Model):

    VISA = 'visa'
    MASTERCARD = 'mastercard'
    AMEX = 'amex'
    DISCOVER = 'discover'
    DEBIT = 'debit'
    CASH = 'cash'

    PAYMENT_TYPE_CHOICES = (
        (VISA, 'Visa'),
        (MASTERCARD, 'Mastercard'),
        (DISCOVER, 'Discover'),
        (AMEX, 'American Express'),
        (DEBIT, 'Debit'),
        (CASH, 'Cash')
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    payment_type = models.CharField(max_length=10, verbose_name=_("Payment type"), choices=PAYMENT_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    key = models.CharField(max_length=255)
    site = models.ForeignKey("sites.Site", editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    tax_type = models.CharField(_("Tax type"), max_length=50, blank=True)
    tax_total = fields.MoneyField(_("Tax total"))
    item_total = fields.MoneyField(_("Item total"))
    total = fields.MoneyField(_("Order total"))
    transaction_id = models.CharField(_("Transaction ID"), max_length=255, null=True,
                               blank=True)

    objects = TransactionManager()

    session_fields = ("tax_type", "tax_total")

    def setup(self, request):

        for field in self.session_fields:
            if field in request.session:
                setattr(self, field, request.session[field])

        if self.tax_total is not None:
            self.total += Decimal(self.tax_total)

        self.total = self.item_total = request.cart.total_price()

        self.save()  # We need an ID before we can add related items.

        for item in request.cart:
            product_fields = [f.name for f in SelectedProduct._meta.fields]
            item = dict([(f, getattr(item, f)) for f in product_fields])
            self.items.create(**item)

    def complete(self, request):
        """
        Remove order fields that are stored in the session, reduce the
        stock level for the items in the order, decrement the uses
        remaining count for discount code (if applicable) and then
        delete the cart.
        """
        self.save()  # Save the transaction ID.
        discount_code = request.session.get('discount_code')
        clear_session(request, "order", *self.session_fields)
        for item in request.cart:
            try:
                variation = ProductVariation.objects.get(sku=item.sku)
            except ProductVariation.DoesNotExist:
                pass
            else:
                variation.update_stock(item.quantity * -1)
                variation.product.actions.purchased()
        if discount_code:
            DiscountCode.objects.active().filter(code=discount_code).update(
                uses_remaining=models.F('uses_remaining') - 1)

        request.cart.delete()
        del request.session['cart']

    def generate_badges(self):
        for item in self.items.all():
            ticket_option = TicketOption.objects.get(sku=item.sku)

            for x in range(0, item.quantity):
                Badge.objects.create_badge(order=None, item=item, ticket_option=ticket_option, transaction=self)


class TransactionItem(SelectedProduct):
    """
    A selected product in a completed order.
    """
    transaction = models.ForeignKey("Transaction", related_name="items")
