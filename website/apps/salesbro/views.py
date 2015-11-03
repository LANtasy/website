from __future__ import unicode_literals, absolute_import

import logging
from cartridge.shop.forms import CartItemFormSet, DiscountForm
from cartridge.shop.views import tax_handler
from mezzanine.conf import settings

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DetailView, RedirectView, TemplateView, FormView, View
from django.contrib.messages import info
from django.utils.translation import ugettext_lazy as _

from cartridge.shop.utils import recalculate_cart
from cartridge.shop.models import Product, ProductVariation, DiscountCode
from braces.views import GroupRequiredMixin
from django.views.generic.base import TemplateResponseMixin

import itertools

from website.apps.salesbro.forms import AddTicketForm, TicketOptionFormSet, ProductVariationFormSet
from website.apps.salesbro.models import Ticket, TicketOption

logger = logging.getLogger(__name__)


class TicketListView(ListView):
    model = Ticket
    template_name = 'salesbro/ticket_list.html'


class TicketDetailView(DetailView):
    queryset = Ticket.objects.filter(available=True)
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    form_class = AddTicketForm

    def get_form_kwargs(self):
        kwargs = {
            'product': self.object,
            'to_cart': True,
        }
        return kwargs

    def get_form(self):
        return self.form_class(self.request.POST or None, **self.get_form_kwargs())

    def get_object(self, queryset=None):
        obj = super(TicketDetailView, self).get_object()
        self.variations = obj.variations.all()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        context = self.get_context_data(add_product_form=form)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['has_available_variations'] = any([v.has_price() for v in self.variations])
        context['images'] = self.object.images.all()
        return context

    def get_queryset(self):
        qs = super(TicketDetailView, self).get_queryset()
        return qs

    def form_valid(self, form):
        quantity = form.cleaned_data["quantity"]
        self.request.cart.add_item(form.ticket_option, quantity)
        recalculate_cart(self.request)
        info(self.request, 'Item added to cart')
        return redirect("shop_cart")

    def form_invalid(self, form):
        context = self.get_context_data(add_product_form=form)
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form=form)
        return self.form_invalid(form=form)


class VendorLogon(GroupRequiredMixin, RedirectView):
    group_required = u'Sales Portal Access'
    url = reverse_lazy('salesbro:vendor_item')
    permanent = False


class VendorItems(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/vendor/items.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        ticket_option_formset = self.get_ticket_option_formset()
        product_formset = self.get_product_formset()

        context['ticket_option_formset'] = ticket_option_formset
        context['product_formset'] = product_formset

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        ticket_option_formset = self.get_ticket_option_formset()
        product_formset = self.get_product_formset()

        ticket_option_formset_valid = ticket_option_formset.is_valid()
        product_formset_valid = product_formset.is_valid()

        quantity = self.get_total_quantity(ticket_option_formset, product_formset)

        if ticket_option_formset_valid and product_formset_valid and quantity > 0:
            return self.formsets_valid(ticket_option_formset, product_formset)
        else:
            return self.formsets_invalid(ticket_option_formset, product_formset, quantity)

    def get_total_quantity(self, *formsets):
        quantity = 0
        for formset in formsets:
            for form in formset:
                quantity += form.cleaned_data.get('quantity', 0)

        return quantity

    def formsets_valid(self, ticket_option_formset, product_formset):

        for form in itertools.chain(ticket_option_formset, product_formset):
            variation = form.cleaned_data['id']
            quantity = form.cleaned_data['quantity']

            if quantity > 0:
                self.request.cart.add_item(variation=variation, quantity=quantity)

        tax_handler(self.request, None)
        recalculate_cart(self.request)

        return redirect('salesbro:vendor_cart')
        # return self.render_to_response(context={})

    def formsets_invalid(self, ticket_option_formset, product_formset, quantity):
        context = self.get_context_data()

        page_errors = []

        if quantity == 0:
            page_errors.append("Invalid quantity.")

        context['page_errors'] = page_errors
        context['ticket_option_formset'] = ticket_option_formset
        context['product_formset'] = product_formset
        return self.render_to_response(context)

    def get_ticket_option_queryset(self):
        queryset = ProductVariation.objects.filter(product_id__in=TicketOption.objects.all())
        return queryset

    def get_product_variation_formset_kwargs(self):
        queryset = self.get_product_variation_queryset()

        kwargs = {
            'queryset': queryset,
            'data': self.request.POST or None,
            'prefix': 'products',
        }

        return kwargs

    def get_product_variation_queryset(self):
        queryset = ProductVariation.objects.all()
        queryset = queryset.exclude(product__in=TicketOption.objects.all())
        queryset = queryset.exclude(product__in=Ticket.objects.all())
        return queryset

    def get_ticket_option_formset_kwargs(self):
        queryset = self.get_ticket_option_queryset()

        kwargs = {
            'queryset': queryset,
            'data': self.request.POST or None,
            'prefix': 'ticket_option',
        }

        return kwargs

    def get_ticket_option_formset(self):
        kwargs = self.get_ticket_option_formset_kwargs()
        formset = TicketOptionFormSet(**kwargs)
        return formset

    def get_product_formset(self):
        kwargs = self.get_product_variation_formset_kwargs()
        formset = ProductVariationFormSet(**kwargs)
        return formset

    def get_context_data(self, **kwargs):

        context = {}

        return context


class VendorCart(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/vendor/cart.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        ticket_option_formset = ''  # self.get_ticket_option_formset()
        cart_formset = self.get_cart_formset()        # self.get_product_formset()

        context['ticket_option_formset'] = ticket_option_formset
        context['cart_formset'] = cart_formset

        return self.render_to_response(context)

    def get_cart_formset_kwargs(self):
        kwargs = {
            'instance': self.request.cart,
            'data': self.request.POST or None,
        }
        return kwargs

    def get_cart_formset(self):
        kwargs = self.get_cart_formset_kwargs()
        formset = CartItemFormSet(**kwargs)
        return formset

    def cart_update_valid(self, cart_formset, product_formset):

        for form in itertools.chain(cart_formset):
            variation = form.cleaned_data['id']
            quantity = form.cleaned_data['quantity']

            if quantity > 0:
                self.request.cart.add_item(variation=variation, quantity=quantity)

        tax_handler(self.request, None)
        recalculate_cart(self.request)

        return redirect('salesbro:vendor_cart')
        # return self.render_to_response(context={})

    def get_context_data(self, **kwargs):

        context = {}

        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('update'):
            return self.post_update()
        elif request.POST.get('back'):
            return self.post_back()
        elif request.POST.get('submit'):
            return self.post_submit()
        else:
            logger.error('Post type invalid')
            raise NotImplementedError

    def post_update(self):
        cart_formset = self.get_cart_formset()
        cart_formset_valid = cart_formset.is_valid()
        cart_session_valid = self.request.cart.has_items()

        if cart_session_valid and cart_formset_valid:
            cart_formset.save()
            recalculate_cart(self.request)
            tax_handler(self.request, None)
            cart_formset.save()
            info(self.request, _("Cart updated"))
            return redirect('salesbro:vendor_cart')
        elif cart_session_valid:
            # Session still active, invalid input
            raise NotImplementedError
        else:
            logger.warn('Session expired')
            # Session timed out
            raise NotImplementedError

    def post_back(self):
        return redirect('salesbro:vendor_item')

    def post_submit(self):
        raise NotImplementedError


@never_cache
def cart(request, template="salesbro/vendor/cart.html", cart_formset_class=CartItemFormSet, discount_form_class=DiscountForm):
    """
    Display cart and handle removing items from the cart.
    """

    cart_formset = cart_formset_class(instance=request.cart)
    discount_form = discount_form_class(request, request.POST or None)
    if request.method == "POST":
        valid = True
        if request.POST.get("update_cart"):
            valid = request.cart.has_items()
            if not valid:
                # Session timed out.
                info(request, _("Your cart has expired"))
            else:
                cart_formset = cart_formset_class(request.POST,
                                                  instance=request.cart)
                valid = cart_formset.is_valid()
                if valid:
                    cart_formset.save()
                    recalculate_cart(request)
                    info(request, _("Cart updated"))
                else:
                    # Reset the cart formset so that the cart
                    # always indicates the correct quantities.
                    # The user is shown their invalid quantity
                    # via the error message, which we need to
                    # copy over to the new formset here.
                    errors = cart_formset._errors
                    cart_formset = cart_formset_class(instance=request.cart)
                    cart_formset._errors = errors
        else:
            valid = discount_form.is_valid()
            if valid:
                discount_form.set_discount()
            # Potentially need to set shipping if a discount code
            # was previously entered with free shipping, and then
            # another was entered (replacing the old) without
            # free shipping, *and* the user has already progressed
            # to the final checkout step, which they'd go straight
            # to when returning to checkout, bypassing billing and
            # shipping details step where shipping is normally set.
            recalculate_cart(request)
        if valid:
            return redirect("shop_cart")
    context = {"cart_formset": cart_formset}
    settings.use_editable()
    if (settings.SHOP_DISCOUNT_FIELD_IN_CART and
            DiscountCode.objects.active().exists()):
        context["discount_form"] = discount_form
    return render(request, template, context)


ticket_detail = TicketDetailView.as_view()
ticket_list = TicketListView.as_view()
vendor_logon = VendorLogon.as_view()
vendor_item = VendorItems.as_view()
vendor_cart = VendorCart.as_view()
