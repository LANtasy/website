import csv
import logging

from braces.views import GroupRequiredMixin
from cartridge.shop.models import Order
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.list import BaseListView
from extra_views import ModelFormSetView

from website.apps.badgebro.forms import BadgeUpdateForm, BadgeUpgradeForm
from website.apps.badgebro.models import Badge, UpgradeTransaction
from website.apps.eventbro.models import Convention, Event, Registration
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


class FrontDeskListView(GroupRequiredMixin, ListView):
    group_required = u'frontdesk'
    template_name = 'badgebro/frontdesk.html'
    queryset = Badge.objects.all().order_by('order_id').only('order', 'first_name', 'last_name', 'uid')
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = super(FrontDeskListView, self).get_queryset()

        if query:
            if query[:1] == '#':
                queryset = queryset.filter(order__id__iexact=query[1:])
            else:
                filters = Q(first_name__icontains=query)
                filters |= Q(last_name__icontains=query)
                filters |= Q(uid__icontains=query)
                queryset = queryset.filter(filters)

        return queryset


class BadgeDetailView(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = u'frontdesk'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = BadgeUpdateForm
    queryset = Badge.objects.all()
    template_name = 'badgebro/badge_detail.html'
    success_message = 'Successfully updated badge'

    def get_success_url(self):
        return reverse('badgebro:badge_detail', kwargs={'uid': self.object.uid})


class BadgeOrderDetailView(GroupRequiredMixin, SuccessMessageMixin, ModelFormSetView):
    group_required = u'frontdesk'
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
        'network'
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


class BadgeUpgradeView(GroupRequiredMixin, SuccessMessageMixin, UpdateView):
    group_required = u'frontdesk'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'
    form_class = BadgeUpgradeForm
    queryset = Badge.objects.select_related('ticket').all()
    template_name = 'badgebro/badge_upgrade.html'
    success_message = 'Successfully upgraded badge'

    def get_success_url(self):
        return reverse('badgebro:badge_detail', kwargs={'uid': self.object.uid})

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


class BadgeOrderUgradeView(BadgeUpgradeView):
    group_required = u'frontdesk'

    def get_success_url(self):
        kwargs = {
            'order_pk': self.object.order_id,
        }

        return reverse('badgebro:badge_order_detail', kwargs=kwargs)


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


class BadgePrintView(GroupRequiredMixin, DetailView):
    group_required = u'frontdesk'
    queryset = Badge.objects.all()
    template_name = 'badgebro/badge_print.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'

    def get(self, request, *args, **kwargs):

        response = super(BadgePrintView, self).get(request, *args, **kwargs)

        return response


class BadgePrintCloseView(BadgePrintView):
    group_required = u'frontdesk'
    queryset = Badge.objects.all()
    template_name = 'badgebro/badge_print_close.html'
    slug_field = 'uid'
    slug_url_kwarg = 'uid'


class BadgeSetPrintedView(GroupRequiredMixin, DetailView):
    group_required = u'frontdesk'
    queryset = Badge.objects.all()
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_printed()

        return JsonResponse({})


class BadgeSetCollectedView(GroupRequiredMixin, DetailView):
    group_required = u'frontdesk'
    queryset = Badge.objects.all()
    slug_url_kwarg = 'uid'
    slug_field = 'uid'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.mark_collected()
        return JsonResponse({})


class OrganizeListView(GroupRequiredMixin, ListView):
    group_required = u'frontdesk'
    queryset = Convention.objects.all()
    template_name = 'badgebro/organize/conventions.html'

    def get_queryset(self):
        queryset = super(OrganizeListView, self).get_queryset()
        queryset = queryset.order_by('start')
        return queryset


class OrganizeEventListView(GroupRequiredMixin, ListView):
    group_required = u'frontdesk'
    queryset = Event.objects.all()
    convention_queryset = Convention.objects.all()
    template_name = 'badgebro/organize/events.html'

    def get_convention(self):
        queryset = self.convention_queryset
        filter_kwargs = {'slug': self.kwargs['convention']}
        convention = get_object_or_404(queryset, **filter_kwargs)
        return convention

    def get_queryset(self):
        convention = self.get_convention()
        queryset = super(OrganizeEventListView, self).get_queryset()
        filter_kwargs = {'convention': convention}
        queryset = queryset.filter(**filter_kwargs)

        if len(queryset) == 0:
            raise Http404

        return queryset


class OrganizeRegistrationsListView(GroupRequiredMixin, ListView):
    group_required = u'frontdesk'
    queryset = Registration.objects.all()
    event_queryset = Event.objects.all()
    template_name = 'badgebro/organize/registrations.html'

    def get_event(self):
        queryset = self.event_queryset

        filter_kwargs = {'slug': self.kwargs['event']}
        event = get_object_or_404(queryset, **filter_kwargs)
        return event

    def get_queryset(self):
        event = self.get_event()
        queryset = super(OrganizeRegistrationsListView, self).get_queryset()
        filter_kwargs = {'event': event}
        queryset = queryset.filter(**filter_kwargs)

        return queryset


class OrganizeRegistrationsExportView(OrganizeRegistrationsListView):
    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.csv"' % (
            self.kwargs['convention'], self.kwargs['event']
        )

        object_list = self.object_list

        writer = csv.writer(response)
        writer.writerow(['Date', 'Time',
                         'First Name',
                         'Last Name',
                         'Email',
                         'Group Name',
                         'Group Captain'])
        for registration in object_list:
            writer.writerow([registration.date_added.date(),
                             registration.date_added.time(),
                             registration.user.first_name or 'None',
                             registration.user.last_name or 'None',
                             registration.user.email or 'None',
                             registration.group_name or 'None',
                             registration.group_captain or 'None'])

        return response


class OrganizeBadgesListView(GroupRequiredMixin, ListView):
    group_required = u'frontdesk'
    queryset = Badge.objects.all()
    template_name = 'badgebro/organize/events.html'

    def get_queryset(self):
        queryset = super(OrganizeBadgesListView, self).get_queryset()

        if self.kwargs.get('filter'):
            if self.kwargs['filter'] == 'unregistered':
                filter_kwargs = {'user': None}
                queryset = queryset.filter(**filter_kwargs)

        return queryset


class OrganizeBadgesExportView(OrganizeBadgesListView):
    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.csv"' % (
            self.kwargs['convention'], 'badges'
        )

        object_list = self.object_list

        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Badge ID', 'User', 'Order Email', 'User Email',
                         'First Name', 'Last Name',
                         'Ticket Type', 'Ticket Option', 'Network'])
        for badge in object_list:
            if badge.order:
                order_id = badge.order.id
                order_email = User.objects.get(id=badge.order.user_id).email
            else:
                order_id = order_email = 'None'

            if badge.user:
                user_name = badge.user.username
                user_email = badge.user.email
            else:
                user_name = user_email = 'None'

            writer.writerow([order_id,
                             badge.uid,
                             user_name,
                             order_email,
                             user_email,
                             badge.first_name or 'None',
                             badge.last_name or 'None',
                             badge.type or 'None',
                             badge.option or 'None',
                             badge.network])

        return response


front_desk = FrontDeskListView.as_view()
badge_detail = BadgeDetailView.as_view()
badge_upgrade = BadgeUpgradeView.as_view()
badge_print = BadgePrintView.as_view()
badge_print_close = BadgePrintCloseView.as_view()

badge_order_upgrade = BadgeOrderUgradeView.as_view()
badge_printed = BadgeSetPrintedView.as_view()
badge_collected = BadgeSetCollectedView.as_view()

organize = OrganizeListView.as_view()
organize_events = OrganizeEventListView.as_view()
organize_registrations = OrganizeRegistrationsListView.as_view()
organize_registrations_export = OrganizeRegistrationsExportView.as_view()
organize_badges = OrganizeBadgesListView.as_view()
organize_badges_export = OrganizeBadgesExportView.as_view()
