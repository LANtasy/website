from __future__ import unicode_literals, absolute_import

import logging
from cartridge.shop import checkout
from cartridge_stripe import billship_handler
from django import forms

from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error, warning

from cartridge.shop.forms import CartItemFormSet, OrderForm
from cartridge.shop.views import tax_handler
from cartridge.shop.utils import recalculate_cart
from cartridge.shop.models import ProductVariation, Product, Order
from cartridge.shop import checkout
from braces.views import GroupRequiredMixin

import itertools
from website.apps.salesbro.checkout import salesbro_order_handler

from website.apps.salesbro.forms import AddTicketForm, TicketOptionFormSet, ProductVariationFormSet
from website.apps.salesbro.models import Ticket, TicketOption

logger = logging.getLogger(__name__)


class TicketListView(ListView):
    model = Ticket
    template_name = 'salesbro/shop/ticket_list.html'
    queryset = Ticket.objects.filter(available=True, status=2)


class TicketDetailView(DetailView):
    queryset = Ticket.objects.filter(available=True, status=2)
    template_name = 'salesbro/shop/ticket_detail.html'
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
        context['is_stock_available'] = self.is_stock_available()
        # ticket_options = TicketOption.objects.available().filter(ticket=self.object)
        # for product_variation in ProductVariation.objects.filter(product=ticket_options):
        #         if not getattr(product_variation, 'has_stock')():
        #             ticket_options = ticket_options.exclude(variations=product_variation)

        # valid_ticket_options = []
        # for ticket_option in ticket_options:
        #     variations = ProductVariation.objects.filter(product=ticket_option)
        #     for variation in variations:
        #         if variation.has_stock():
        #             print variation
        #     # if any([v.has_stock() for v in variations]):
        #     #     valid_ticket_options.append(ticket_option)
        #
        #     # if any([v.has_stock() for v in ticket_option.variations]):
        #
        # context['ticket_options'] = ticket_options
        return context

    def is_stock_available(self):
        ticket_options = TicketOption.objects.available().filter(ticket=self.object)

        for product_variation in ProductVariation.objects.filter(product=ticket_options):
            if not getattr(product_variation, 'has_stock')():
                ticket_options = ticket_options.exclude(variations=product_variation)

        if ticket_options.count() > 0:
            return True
        else:
            return False

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


class PortalLogon(GroupRequiredMixin, RedirectView):
    group_required = u'Sales Portal Access'
    url = reverse_lazy('salesbro:portal_item')
    permanent = False


class PortalItems(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/portal/items.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        ticket_option_formset = self.get_ticket_option_formset()
        product_formset = self.get_product_formset()

        context['ticket_option_formset'] = ticket_option_formset
        context['product_formset'] = product_formset

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('go_to_cart'):
            return redirect('salesbro:portal_cart')
        else:
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

            try:
                # If it's a ticket option
                variation = form.ticket_option
            except AttributeError:
                # If it's a product already
                variation = form.cleaned_data['id']
            quantity = form.cleaned_data['quantity']

            if quantity > 0:
                self.request.cart.add_item(variation=variation, quantity=quantity)

        tax_handler(self.request, None)
        recalculate_cart(self.request)

        return redirect('salesbro:portal_cart')
        # return self.render_to_response(context={})

    def formsets_invalid(self, ticket_option_formset, product_formset, quantity):
        context = self.get_context_data()

        if quantity == 0:
            error(self.request, 'Invalid quantity.')

        context['ticket_option_formset'] = ticket_option_formset
        context['product_formset'] = product_formset
        return self.render_to_response(context)

    def get_ticket_option_queryset(self):
        queryset = TicketOption.objects.available().order_by('ticket')
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
        queryset = queryset.filter(product__available=True)
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


class PortalCart(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/portal/cart.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        cart_formset = self.get_cart_formset()
        context['cart_formset'] = cart_formset

        order_form = self.get_order_form(checkout.CHECKOUT_STEP_FIRST)
        context['order_form'] = order_form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if self.request.cart.has_items():
            context = self.update_formset()

        if request.POST.get('update'):
            return redirect('salesbro:portal_cart')
        elif request.POST.get('back'):
            return redirect('salesbro:portal_item')
        elif request.POST.get('order'):
            return self.submit_order(context)
        else:
            logger.error('Post type invalid')
            raise NotImplementedError

    def submit_order(self, context):
        order_form = context['order_form']

        # Double check that order still has things
        if self.request.cart.has_items() is False:
            warning(self.request, _("Cart is empty"))
            return redirect('salesbro:portal_cart')

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.setup(self.request)
            # TODO: Make transaction_id link to payment type somehow
            order.transaction_id = self.request.POST.get('payment_type')
            order.complete(self.request)
            salesbro_order_handler(request=self.request, order_form=order, order=order)
            checkout.send_order_email(request=self.request, order=order)
            return redirect('salesbro:portal_complete')
        else:
            return self.render_to_response(context=context)

    def update_formset(self):
        cart_formset = self.get_cart_formset()

        if self.request.cart.has_items() is False:
            warning(self.request, _("Cart is empty"))
        elif cart_formset.is_valid():
            cart_formset.save()
            recalculate_cart(self.request)
            billship_handler(self.request, None)
            tax_handler(self.request, None)
            info(self.request, _('Cart updated'))
        else:
            error(self.request, _('Invalid cart update'))

        order_form = self.get_order_form(checkout.CHECKOUT_STEP_FIRST)

        if order_form.is_valid():
            self.request.session['order'] = dict(order_form.cleaned_data)
        else:
            error(self.request, _('Invalid customer details'))

        context = self.get_context_data()
        context['cart_formset'] = self.get_cart_formset()
        context['order_form'] = order_form

        return context

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

    def get_order_form_kwargs(self, step):
        try:
            initial = self.request.session['order']
        except KeyError:
            initial = {
                   'remember': False,
                'same_billing_shipping': True,
                'shipping_detail_first_name': 'N/A',
                'shipping_detail_last_name': 'N/A',
                'shipping_detail_street': 'N/A',
                'shipping_detail_city': 'N/A',
                'shipping_detail_state': 'N/A',
                'shipping_detail_postcode': 'N/A',
                'shipping_detail_country': 'N/A',
                'shipping_detail_phone': 'N/A',
                'shipping_detail_email': 'N/A',
                'billing_detail_street': 'N/A',
                'billing_detail_city': 'N/A',
                'billing_detail_state': 'N/A',
                'billing_detail_postcode': 'N/A',
                'billing_detail_country': 'N/A',
                'additional_instructions': 'N/A',
           }

        kwargs = {
            'initial': initial,
            'request': self.request or None,
            'data': self.request.POST or None,
            'step': step or None,
        }
        return kwargs

    def get_form_class(self):
        return OrderForm

    def get_order_form(self, step):

        VISA = 'visa'
        MASTERCARD = 'mastercard'
        AMEX = 'amex'
        DISCOVER = 'discover'
        DEBIT = 'debit'
        CASH = 'cash'

        PAYMENT_CHOICES = (
            (None, '---------'),
            (CASH, 'Cash'),
            (DEBIT, 'Debit'),
            (VISA, 'Visa'),
            (MASTERCARD, 'Mastercard'),
            (DISCOVER, 'Discover'),
            (AMEX, 'American Express'),
        )

        kwargs = self.get_order_form_kwargs(step)
        form = OrderForm(**kwargs)
        form.fields['payment_type'] = forms.ChoiceField(choices=PAYMENT_CHOICES)
        return form

    def get_context_data(self, **kwargs):
        context = {}
        return context


class PortalComplete(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/portal/complete.html'

    def get_context_data(self, **kwargs):
        order = self.get_order()

        context = {'order': order, 'has_pdf': False}

        return context

    def get_order(self):
        try:
            order = Order.objects.from_request(self.request)
        except Order.DoesNotExist:
            raise NotImplementedError

        return order


ticket_detail = TicketDetailView.as_view()
ticket_list = TicketListView.as_view()
portal_logon = PortalLogon.as_view()
portal_item = PortalItems.as_view()
portal_cart = PortalCart.as_view()
portal_complete = PortalComplete.as_view()
