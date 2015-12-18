from braces.views import LoginRequiredMixin
from django.contrib.messages import error
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, RedirectView
from website.apps.badgebro.models import Badge
from website.apps.eventbro.forms import UpdateUserForm, UpdateBadgeForm
from website.apps.eventbro.models import Event, Registration


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
                badge.user = self.request.user
                badge.save()
                return True
            except Badge.DoesNotExist:
                error(self.request, 'Could not find UID')
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


class RegisterEventView(LoginRequiredMixin, TemplateView):
    template_name = 'eventbro/registration/register_event.html'

    def get(self, request, *args, **kwargs):
        url = self.check_badges_for_user()
        if url:
            return HttpResponseRedirect(url)
        else:
            return self.display_page()

    def display_page(self):
        context = self.reset_context()
        context['event_categories'] = self.get_event_categories()
        # context['event_categories_empty'] = self.get_empty_categories(categories)
        context['published_events'] = self.get_events()
        context['registered_events'] = self.get_registered_events()

        return self.render_to_response(context)

    def check_badges_for_user(self):
        user = self.request.user
        try:
            Badge.objects.get(user=user)
            url = None
        except Badge.DoesNotExist:
            url = reverse_lazy('eventbro:register_badge')
        return url

    def get_events(self):
        events = Event.objects.filter(valid_options__badges__user=self.request.user, published=True)
        events = events.order_by('name')
        return events

    def get_empty_categories(self, categories):
        empty = ''
        events = self.get_events()

        for category in categories:

            events = Event.objects.filter(event_type=category[0])
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

    def get_registered_events(self):
        try:
            events = Event.objects.filter(registration_event__user=self.request.user)
        except Registration.DoesNotExist:
            events = None
        return events

    @staticmethod
    def reset_context():
        context = {}
        return context

    # return in context the registered events
    # return in context all of the events (with some standard filters)
    # write function on event - that checks if space available
    # on template is the event open and is the event in the list of already registered

    # post to eventID, check for room, then register

    # TODO: If time conflict display warning
    # TODO: Allow user to remove badge associated with their account
    # TODO: Allow user to unregister from an event
    # TODO: Allow user to generate their event calendar

    # - Sort into the 4 different categories
    # - Maybe add filter for categories
    # - Show event, and time run
    # - Lookup user's registrations, render unregister button
    #       (registered - boolean? or just delete object?)
    # - If event is full, render waitlist button

    # - Lookup conventions that are published
    #   - Lookup events that are published associated with those conventions
    #       -Lookup if event is available for the associated badge
    #            -List all of the events that meet these criteria
    #                -If regular event, display register button, if full display waitlist button
    #                -if special event, display same as regular event, display additional required fields

register_redirect = RegisterRedirectView.as_view()
register_badge = RegisterBadgeView.as_view()
register_event = RegisterEventView.as_view()
