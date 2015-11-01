from __future__ import unicode_literals, absolute_import

import logging

from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView, TemplateView, FormView
from django.contrib.messages import info
from django.http import HttpResponse

from cartridge.shop.utils import recalculate_cart
from cartridge.shop.models import Product
from braces.views import GroupRequiredMixin
from extra_views import FormSetView, InlineFormSet, CreateWithInlinesView
from extra_views.generic import GenericInlineFormSet

from website.apps.salesbro.forms import AddTicketForm
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
    url = reverse_lazy('salesbro:vendor_cart')
    permanent = False


class VendorCart(GroupRequiredMixin, FormSetView):
    group_required = u'Sales Portal Access'
    form_class = ''
    template_name = 'salesbro/vendor/cart.html'


    def get_context_data(self, **kwargs):
        context = super(VendorCart, self).get_context_data(**kwargs)

        return context



'''
class VendorCart(GroupRequiredMixin, ListView):
    group_required = u'Sales Portal Access'
    template_name = 'salesbro/vendor/cart.html'

    # On GET display 2 separate sections (TicketOptions, Products)
    # Display as 2 separate formsets (TicketOptions, Products)
    # Display each item (item name, price, quantity
    # Two POST types (Update Cart, Go to Checkout)
    # Update cart: Calculates individual item totals, calculates all totals, calculates tax, calculates discount
    # Checkout cart: For each item with qty>0 create cart item

    def get_queryset(self):
        return Product.objects.order_by('title')

    def get_context_data(self, **kwargs):
        context = super(VendorCart, self).get_context_data(**kwargs)
        context['ticket_option_list'] = TicketOption.objects.order_by('title')
        context['ticket_list'] = Ticket.objects.order_by('title')
        product_queryset = Product.objects.order_by('title')
        product_queryset = product_queryset.exclude(id__in=TicketOption.objects.all())
        product_queryset = product_queryset.exclude(id__in=Ticket.objects.all())
        context['product_list'] = product_queryset
        return context
'''

class VendorCheckout(GroupRequiredMixin, TemplateView):
    group_required = u'Sales Portal Access'

    def get(self, request):
        return HttpResponse('Hello World3')



