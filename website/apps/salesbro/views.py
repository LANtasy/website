from __future__ import unicode_literals, absolute_import

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.contrib.messages import info

from cartridge.shop.utils import recalculate_cart

from website.apps.salesbro.forms import AddTicketForm
from website.apps.salesbro.models import Ticket, TicketOption
from cartridge.shop.models import Product
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from braces.views import LoginRequiredMixin, GroupRequiredMixin

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


class VendorLogon(GroupRequiredMixin, View):
    name = 'vendor_logon'
    group_required = u'Sales Portal Access'

    def get(self, request):
        return redirect('cart/')


class VendorCart(GroupRequiredMixin, ListView):
    name = 'vendor_cart'
    group_required = u'Sales Portal Access'
    context_object_name = 'all_product_list'
    template_name = 'salesbro/vendor/cart.html'

    def get_queryset(self):
        return Product.objects.order_by('title')

    def get_context_data(self, **kwargs):
        context = super(VendorCart, self).get_context_data(**kwargs)
        context['ticket_option_list'] = TicketOption.objects.order_by('title')
        context['ticket_list'] = Ticket.objects.order_by('title')
        products = Product.objects.order_by('title')
        product_list = []
        for product in products:
            if product not in context['ticket_option_list']:
                print context['ticket_option_list']
                product_list.append(product)
                print product

        context['product_list'] = product_list

        return context


class VendorCheckout(GroupRequiredMixin, TemplateView):
    name = 'vendor_checkout'
    group_required = u'Sales Portal Access'

    def get(self, request):
        return HttpResponse('Hello World3')

ticket_list = TicketListView.as_view()
ticket_detail = TicketDetailView.as_view()


