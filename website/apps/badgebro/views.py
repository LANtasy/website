from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import ListView, UpdateView, DetailView

from website.apps.badgebro.forms import BadgeUpdateForm, BadgeUpgradeForm
from website.apps.badgebro.models import Badge, UpgradeTransaction
from website.apps.salesbro.models import TicketOption


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

front_desk = FrontDeskListView.as_view()
badge_detail = BadgeDetailView.as_view()
badge_upgrade = BadgeUpgradeView.as_view()
badge_print = BadgePrintView.as_view()
