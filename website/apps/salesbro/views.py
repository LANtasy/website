from __future__ import unicode_literals, absolute_import

import logging

from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import info, error, warning

from cartridge.shop.forms import CartItemFormSet
from cartridge.shop.views import tax_handler
from cartridge.shop.utils import recalculate_cart
from cartridge.shop.models import ProductVariation
from braces.views import GroupRequiredMixin

import itertools

from website.apps.salesbro.forms import AddTicketForm, TicketOptionFormSet, ProductVariationFormSet, CustomerForm
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


class PortalCart(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/portal/cart.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        cart_formset = self.get_cart_formset()
        context['cart_formset'] = cart_formset

        order_form = self.get_order_form()
        context['order_form'] = order_form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.update_formset()

        if request.POST.get('update'):
            return self.render_to_response(context)
        elif request.POST.get('back'):
            return redirect('salesbro:portal_item')
        elif request.POST.get('order'):
            return self.update_formset
        else:
            logger.error('Post type invalid')
            raise NotImplementedError

    def update_formset(self):
        cart_formset = self.get_cart_formset()
        order_form = self.get_order_form()

        if not self.request.cart.has_items():
            warning(self.request, _("Your session has timed out"))
        elif cart_formset.is_valid() and order_form.is_valid():
            cart_formset.save()
            recalculate_cart(self.request)
            tax_handler(self.request, None)
            info(self.request, _('Cart updated'))
        else:
            error(self.request, _('Invalid update'))

        context = self.get_context_data()
        context['cart_formset'] = cart_formset
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


    def get_order_form_kwargs(self):
        # TODO: Fix this, need to save instance so the session persists if user browses away from page.
        try:
            kwargs = {
                'instance': self.request.order,
                'data': self.request.POST or None,
            }
        except AttributeError:
            kwargs = {
                'data': self.request.POST or None,
            }
        return kwargs

    def get_order_form(self):
        kwargs = self.get_order_form_kwargs()
        form = CustomerForm(**kwargs)
        return form

    def get_context_data(self, **kwargs):
        context = {}
        return context


class PortalCheckout(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/portal/checkout.html'



    '''
    Goals:
    -Grab remaining order details:
    --Required:
    ---First Name, Last Name, Phone, Email
    --Optional: Try to save without this, otherwise input fake data
    ---Street, City, Province/State, Postal Code/Zip, Country

    -Deal with shipping? See how cartridge deals with this

    '''


ticket_detail = TicketDetailView.as_view()
ticket_list = TicketListView.as_view()
portal_logon = PortalLogon.as_view()
portal_item = PortalItems.as_view()
portal_cart = PortalCart.as_view()
portal_checkout = PortalCheckout.as_view()
