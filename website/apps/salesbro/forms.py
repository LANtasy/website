from __future__ import unicode_literals, absolute_import

import logging

from cartridge.shop.forms import AddProductForm, ADD_PRODUCT_ERRORS, ProductAdminForm
from cartridge.shop.models import ProductVariation

from django import forms
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


class TicketOptionAdminForm(ProductAdminForm):
    class Meta:
        model = TicketOption
        exclude = []


class TicketOptionChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return '{name} +${price}'.format(name=obj.title, price=obj.pricediff)

    def __init__(self, *args, **kwargs):
        queryset = TicketOption.objects.available()
        super(TicketOptionChoiceField, self).__init__(queryset=queryset, *args, **kwargs)


class AddTicketForm(AddProductForm):

    ticket_option = TicketOptionChoiceField()

    def __init__(self, *args, **kwargs):
        super(AddTicketForm, self).__init__(*args, **kwargs)
        if self._product is not None:
            self.fields['ticket_option'].queryset = TicketOption.objects.available().filter(ticket=self._product)

    def clean(self):
        """
        Determine the chosen variation, validate it and assign it as
        an attribute to be used in views.
        """
        if not self.is_valid():
            return
        # Posted data will either be a sku, or product options for
        # a variation.
        data = self.cleaned_data.copy()
        quantity = data.pop("quantity")
        ticket_option = data.pop('ticket_option')

        # Ensure the product has a price if adding to cart.
        if self._to_cart:
            data["unit_price__isnull"] = False
        error = None
        if self._product is not None:
            # Chosen options will be passed to the product's
            # variations.
            qs = self._product.variations
        else:
            # A product hasn't been given since we have a direct sku.
            qs = ProductVariation.objects

        try:
            variation = qs.get(**data)
        except ProductVariation.DoesNotExist:
            error = "invalid_options"
        else:
            # Validate stock if adding to cart.
            if self._to_cart:
                if not variation.has_stock():
                    error = "no_stock"
                elif not variation.has_stock(quantity):
                    error = "no_stock_quantity"
        if error is not None:
            raise forms.ValidationError(ADD_PRODUCT_ERRORS[error])


        ticket_option_qs = ticket_option.variations

        try:
            ticket_variation = ticket_option_qs.get(**data)
        except ProductVariation.DoesNotExist:
            error = "invalid_ticket_option"
        else:
            # Validate stock if adding to cart.
            if self._to_cart:
                if not variation.has_stock():
                    error = "no_stock"
                elif not variation.has_stock(quantity):
                    error = "no_stock_quantity"
        if error is not None:
            raise forms.ValidationError(ADD_PRODUCT_ERRORS[error])

        self.variation = variation
        self.ticket_option = ticket_variation
        return self.cleaned_data
