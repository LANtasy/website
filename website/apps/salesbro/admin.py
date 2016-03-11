from __future__ import unicode_literals, absolute_import
from copy import deepcopy

import logging
from cartridge.shop.admin import product_list_display, other_product_fields, ProductImageAdmin, ProductVariationAdmin, \
    product_fieldsets, ProductAdmin, option_fields, OrderAdmin
from cartridge.shop.admin import product_list_editable
from cartridge.shop.forms import ProductAdminForm
from cartridge.shop.models import ProductImage, ProductVariation, Order

from django.contrib import admin
from django.utils.translation import ugettext as _
from mezzanine.core.admin import DisplayableAdmin
from website.apps.salesbro.forms import TicketOptionAdminForm

from website.apps.salesbro.models import Ticket, TicketOption
from import_export.admin import ExportMixin

logger = logging.getLogger(__name__)


class TicketAdmin(DisplayableAdmin):

    class Media:
        js = ("cartridge/js/admin/product_variations.js",)
        css = {"all": ("cartridge/css/admin/product.css",)}

    list_display = product_list_display
    list_display_links = ("admin_thumb", "title")
    list_editable = product_list_editable
    list_filter = ("status", "available", "categories")
    filter_horizontal = ("categories",) + tuple(other_product_fields)
    search_fields = ("title", "content", "categories__title",
                     "variations__sku")
    inlines = (ProductImageAdmin, ProductVariationAdmin)
    form = ProductAdminForm
    fieldsets = product_fieldsets

    def save_model(self, request, obj, form, change):
        """
        Store the product object for creating variations in save_formset.
        """
        super(TicketAdmin, self).save_model(request, obj, form, change)
        self._product = obj

    def save_formset(self, request, form, formset, change):
        """

        Here be dragons. We want to perform these steps sequentially:

        - Save variations formset
        - Run the required variation manager methods:
          (create_from_options, manage_empty, etc)
        - Save the images formset

        The variations formset needs to be saved first for the manager
        methods to have access to the correct variations. The images
        formset needs to be run last, because if images are deleted
        that are selected for variations, the variations formset will
        raise errors when saving due to invalid image selections. This
        gets addressed in the set_default_images method.

        An additional problem is the actual ordering of the inlines,
        which are in the reverse order for achieving the above. To
        address this, we store the images formset as an attribute, and
        then call save on it after the other required steps have
        occurred.

        """

        # Store the images formset for later saving, otherwise save the
        # formset.
        if formset.model == ProductImage:
            self._images_formset = formset
        else:
            super(TicketAdmin, self).save_formset(request, form, formset,
                                                   change)

        # Run each of the variation manager methods if we're saving
        # the variations formset.
        if formset.model == ProductVariation:

            # Build up selected options for new variations.
            options = dict([(f, request.POST.getlist(f)) for f in option_fields
                             if request.POST.getlist(f)])
            # Create a list of image IDs that have been marked to delete.
            deleted_images = [request.POST.get(f.replace("-DELETE", "-id"))
                for f in request.POST
                if f.startswith("images-") and f.endswith("-DELETE")]

            # Create new variations for selected options.
            self._product.variations.create_from_options(options)
            # Create a default variation if there are none.
            self._product.variations.manage_empty()

            # Remove any images deleted just now from variations they're
            # assigned to, and set an image for any variations without one.
            self._product.variations.set_default_images(deleted_images)

            # Save the images formset stored previously.
            super(TicketAdmin, self).save_formset(request, form,
                                                 self._images_formset, change)

            # Run again to allow for no images existing previously, with
            # new images added which can be used as defaults for variations.
            self._product.variations.set_default_images(deleted_images)

            # Copy duplicate fields (``Priced`` fields) from the default
            # variation to the product.
            self._product.copy_default_variation()


ticket_fieldsets = deepcopy(TicketAdmin.fieldsets)
ticket_fieldsets[0][1]["fields"].insert(-2, 'ticket')


class TicketOptionAdmin(ProductAdmin):
    fieldsets = ticket_fieldsets
    list_display = product_list_display = ["admin_thumb", "title", "status", "available",
                        "admin_link", "ticket"]

    list_filter = ("status", "available", "categories", "ticket")


order_fieldsets = deepcopy(OrderAdmin.fieldsets)
order_fieldsets[0][1]["fields"].insert(-2, 'user_id')


class CustomOrderAdmin(ExportMixin, OrderAdmin):
    fieldsets = order_fieldsets
    list_filter = ('status', 'time', 'user_id')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketOption, TicketOptionAdmin)
admin.site.unregister(Order)
admin.site.register(Order, CustomOrderAdmin)
