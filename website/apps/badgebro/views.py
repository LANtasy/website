import logging

from cartridge.shop.models import Order
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import ListView, UpdateView, DetailView
from extra_views import ModelFormSetView

from website.apps.badgebro.forms import BadgeUpdateForm, BadgeUpgradeForm
from website.apps.badgebro.models import Badge, UpgradeTransaction
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


class FrontDeskListView(ListView):
    template_name = 'badgebro/frontdesk.html'
    queryset = Badge.objects.all().order_by('order_id')
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('search')
        order = self.request.GET.get('order')
        queryset = super(FrontDeskListView, self).get_queryset()

        if query:
            filters = Q(first_name__icontains=query)
            filters |= Q(last_name__icontains=query)
            filters |= Q(uid__icontains=query)

            queryset = queryset.filter(filters)

        if order:
            queryset = queryset.filter(order__id__iexact=order)

        return queryset


class BadgeDetailView(SuccessMessageMixin, UpdateView):

    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = BadgeUpdateForm
    queryset = Badge.objects.all()
    template_name = 'badgebro/badge_detail.html'
    success_message = 'Successfully updated badge'

    def get_success_url(self):
        return reverse('badge_detail', kwargs={'uid': self.object.uid})


class BadgeOrderDetailView(SuccessMessageMixin, ModelFormSetView):
    queryset = Badge.objects.all()
    order_queryet = Order.objects.all()
    form_class = BadgeUpdateForm
    template_name = 'badgebro/badge_order_detail.html'
    model = Badge
    success_message = 'Successfully updated badges'
    extra = 0
    fields = (
        'first_name',
        'last_name',
        'type'
    )

    def formset_valid(self, formset):

        response = super(BadgeOrderDetailView, self).formset_valid(formset)
        success_message = self.get_success_message({})
        if success_message:
            messages.success(self.request, success_message)

        return response

    def get_order(self):
        queryset = self.order_queryet
        filter_kwargs = {'id': self.kwargs['order_pk']}
        order = get_object_or_404(queryset, **filter_kwargs)
        return order

    def get_queryset(self):
        self.order = self.get_order()
        queryset = super(BadgeOrderDetailView, self).get_queryset()
        filter_kwargs = {'order': self.order}
        queryset = queryset.filter(**filter_kwargs)

        if len(queryset) == 0:
            raise Http404

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BadgeOrderDetailView, self).get_context_data(**kwargs)
        context['order'] = self.order
        return context

badge_order_detail = BadgeOrderDetailView.as_view()


class BadgeUpgradeView(SuccessMessageMixin, UpdateView):

    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = BadgeUpgradeForm
    queryset = Badge.objects.select_related('ticket').all()
    template_name = 'badgebro/badge_upgrade.html'
    success_message = 'Successfully upgraded badge'

    def get_success_url(self):
        return reverse('badge_detail', kwargs={'uid': self.object.uid})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form(self.get_form_class())

        if form.is_valid():

            old_ticket = self.object.ticket
            new_ticket = form.cleaned_data['new_ticket_option']

            upgrade = UpgradeTransaction()
            upgrade.old_ticket = old_ticket
            upgrade.new_ticket = new_ticket
            upgrade.badge = self.object
            upgrade.payment_method = form.cleaned_data['payment_method']
            upgrade.save()

            return self.form_valid(form=form)

        else:
            return self.form_invalid(form)


def badge_difference(request, uid, ticket_id):

    if not request.user.is_authenticated():
        raise PermissionDenied

    badge_queryset = Badge.objects.select_related('ticket').all()
    ticket_queryset = TicketOption.objects.all()

    badge = get_object_or_404(badge_queryset, uid=uid)
    ticket = get_object_or_404(ticket_queryset, id=ticket_id)

    new_price = int(ticket.price() * 100)
    current_price = int(badge.ticket.price() * 100)

    difference = new_price - current_price

    gst = int(difference * 0.05)

    difference = int(difference) / 100.0
    gst = gst / 100.0

    data = dict()
    data['new_price'] = ticket.price()
    data['difference'] = format(difference, '.2f')
    data['gst'] = format(gst, '.2f')
    data['total'] = format(difference + gst, '.2f')

    return JsonResponse(data=data)


class BadgePrintView(DetailView):
    queryset = Badge.objects.all()
    template_name = 'badgebro/badge_print.html'

    def get(self, request, *args, **kwargs):

        response = super(BadgePrintView, self).get(request, *args, **kwargs)

        return response


class BadgeSetPrintedView(DetailView):
    queryset = Badge.objects.all()
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_printed()
        return JsonResponse({})


class BadgeSetCollectedView(DetailView):
    queryset = Badge.objects.all()
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_collected()
        return JsonResponse({})




front_desk = FrontDeskListView.as_view()
badge_detail = BadgeDetailView.as_view()
badge_upgrade = BadgeUpgradeView.as_view()
badge_print = BadgePrintView.as_view()

badge_printed = BadgeSetPrintedView.as_view()
badge_collected = BadgeSetCollectedView.as_view()
