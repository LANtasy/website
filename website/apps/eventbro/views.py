import logging

from braces.views import LoginRequiredMixin
from django.contrib.messages import error, warning, info, success
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.views.generic import TemplateView, RedirectView, UpdateView
from website.apps.badgebro.models import Badge
from website.apps.eventbro.forms import UpdateUserForm, UpdateBadgeForm, RegistrationUpdateForm
from website.apps.eventbro.models import Event, Registration, EventType

logger = logging.getLogger(__name__)

CHECKBOX_MAPPING = {'on': True, 'off': False, }


class EventRegistrationMixin(object):

    queryset = Event.objects.filter(published=True)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    category = None

    def get_queryset(self):
        return self.queryset

    def get_events(self):
        queryset = self.get_queryset()
        queryset = queryset.filter(valid_options__badges__user=self.request.user)
        queryset = queryset.order_by('event_type', 'start')

        if self.category:
            if self.category == 'REG':
                queryset = queryset.filter(registrants__user=self.request.user)
            else:
                queryset = queryset.filter(event_type=self.category)
        return queryset


class RegisterRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        try:
            Badge.objects.get(user=user)
            url = reverse_lazy('eventbro:register_event')
        except Badge.DoesNotExist:
            url = reverse_lazy('eventbro:register_badge')
        return url


class RegisterBadgeView(LoginRequiredMixin, TemplateView):
    template_name = 'eventbro/registration/register_badge.html'

    def get(self, request, *args, **kwargs):
        url = self.check_badges_for_user()
        if url:
            return HttpResponseRedirect(url)
        else:
            return self.display_page()

    def post(self, request, *args, **kwargs):
        url = self.check_badges_for_user()
        if url:
            return HttpResponseRedirect(url)
        else:
            return self.save_forms()

    def save_forms(self):
        return self.check_update(user_valid=self.update_user(),
                                 badge_valid=self.update_badge(),
                                 )

    def check_update(self, user_valid, badge_valid):
        if user_valid and badge_valid:
            already_registered = self.check_badges_for_user()
            if already_registered:
                return HttpResponseRedirect(already_registered)
            else:
                return self.display_page()
        else:
            return self.display_page()

    def invalid_update(self):
        pass

    def update_user(self):
        user_form = self.get_user_form()
        user_form_valid = user_form.is_valid()
        if user_form_valid:
            user_form.save()
            return True
        else:
            return False

    def update_badge(self):
        badge_form = self.get_badge_form()
        badge_form_valid = badge_form.is_valid()
        if badge_form_valid:
            try:
                uid = badge_form.cleaned_data['uid']
                badge = Badge.objects.get(uid=uid)
                if badge.user is not None:
                    error(self.request, 'This badge is already in use')
                    return False
                badge.user = self.request.user
                badge.save()
                return True
            except Badge.DoesNotExist:
                error(self.request, 'Could not find this badge')
                return False
        else:
            return False

    def display_page(self):
        context = self.reset_context()
        context['user_form'] = self.get_user_form()
        context['badge_form'] = self.get_badge_form()
        return self.render_to_response(context)

    # Check to see if the user is already associated with a badge
    # If they are then provide a redirect url
    def check_badges_for_user(self):
        user = self.request.user
        try:
            Badge.objects.get(user=user)
            url = reverse_lazy('eventbro:register_event')
        except Badge.DoesNotExist:
            url = None
        return url

    def get_user_form_kwargs(self):
        kwargs = {
            'instance': self.request.user,
            'data': self.request.POST or None,
        }
        return kwargs

    def get_user_form(self):
        kwargs = self.get_user_form_kwargs()
        form = UpdateUserForm(**kwargs)
        return form

    def get_badge_form_kwargs(self):
        kwargs = {
            'data': self.request.POST or None,
        }
        return kwargs

    def get_badge_form(self):
        kwargs = self.get_badge_form_kwargs()
        form = UpdateBadgeForm(**kwargs)
        return form

    @staticmethod
    def reset_context():
        context = {}
        return context


class RegisterEventView(LoginRequiredMixin, EventRegistrationMixin, TemplateView):
    template_name = 'eventbro/registration/register_event.html'
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = request.GET.get('category', '')
        return super(RegisterEventView, self).dispatch(request, *args, **kwargs)

    def get_event(self):
        """
        Fetches an event within the defined queryset using the defined lookup parameters
        """
        queryset = self.get_events()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        return get_object_or_404(queryset, **filter_kwargs)

    def get(self, request, *args, **kwargs):
        url = self.check_badges_for_user()

        request.user.events = Event.objects.filter(registrants__user=request.user)

        if url:
            return HttpResponseRedirect(url)

        return self.render_to_response(context=self.get_context_data())

    def post(self, request, *args, **kwargs):

        event = self.get_event()

        if 'register' in request.POST:
            return self.register_for_event(event=event)
        elif 'unregister' in request.POST:
            return self.unregister_for_event(event=event)
        else:
            warning(self.request, "You performed an invalid action.")
            return self.render_to_response(context=self.get_context_data())

    def get_context_data(self, **kwargs):
        context = dict()
        context['event_categories'] = EventType.CHOICES
        context['event_forms'] = self.get_event_forms()
        context['filter_category'] = self.category
        context.update(**kwargs)
        return context

    def get_success_url(self):
        url = '%s?category=%s' % (reverse('eventbro:register_event'), self.category)
        return url

    def unregister_for_event(self, event):
        """
        Un-registers a user from an event.  Does nothing if the user is not currently registered.
        """
        event.unregister(user=self.request.user)

        return HttpResponseRedirect(self.get_success_url())

    def register_for_event(self, event):
        """
        Registers a user for an event.  If the event is full wait lists and informs the registrant.
        """
        form_class = event.get_registration_form_class()
        form = form_class(event=event, data=self.request.POST)

        if form.is_valid():

            if event.is_full():
                logger.debug("Event %s full, waitlisting user %s", event.id, self.request.user.id)
                warning(self.request, 'Event was full when registering, you have been waitlisted')

            form.save(user=self.request.user)

        else:
            context = self.get_context_data()
            forms = context['event_forms']

            # Replace blank event form with filled out form + errors
            for index, reg_form in enumerate(forms):
                if reg_form.event.id == event.id:
                    forms[index] = form
                    break

            context['event_forms'] = forms
            self.request.user.events = Event.objects.filter(registrants__user=self.request.user)

            return self.render_to_response(context=context)

        return HttpResponseRedirect(self.get_success_url())

    def check_badges_for_user(self):
        user = self.request.user
        try:
            Badge.objects.get(user=user)
            url = None
        except Badge.DoesNotExist:
            url = self.get_success_url()
        return url

    def get_event_forms(self):

        queryset = self.get_events()
        return [event.get_blank_registration_form() for event in queryset]

    def get_empty_categories(self, categories):
        empty = ''
        events = self.get_events()

        for category in categories:
            events = events.filter(event_type=category[0])
            if events is None:
                empty += events
        return empty

    # Only returns categories based on get_events()
    def get_event_categories(self):
        categories = ()
        events = self.get_events()
        for category in Event.EVENT_TYPE_CHOICES:
            value = events.filter(event_type=category[0])
            if value:
                categories = categories + (category,)
        return categories

    def get_event_form_kwargs(self):
        kwargs = {
            'data': self.request.POST or None
        }
        return kwargs

    # TODO: If time conflict display warning
    # TODO: Allow user to remove badge associated with their account
    # TODO: Allow user to generate their event calendar
    # TODO: Limit based on published Conventions

    # - Maybe add filter for categories


class RegistrationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'eventbro/registration/registration_update.html'
    queryset = Registration.objects.all()
    lookup_field = 'event_id'
    pk_url_kwarg = 'event_id'
    form_class = RegistrationUpdateForm
    success_url = reverse_lazy('eventbro:register_event')

    def get_queryset(self):
        queryset = super(RegistrationUpdateView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.pk_url_kwarg]}

        registration = get_object_or_404(queryset, **filter_kwargs)

        return registration



register_redirect = RegisterRedirectView.as_view()
register_badge = RegisterBadgeView.as_view()
register_event = RegisterEventView.as_view()

registration_detail = RegistrationUpdateView.as_view()
