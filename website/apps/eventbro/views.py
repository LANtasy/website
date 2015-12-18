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

    def post(self, request, *args, **kwargs):
        button = self.get_button_pressed(request)
        action, event_id = button.split('-')

        if action == 'register':
            return self.register_for_event(event_id)
        elif action == 'unregister':
            return self.unregister_for_event(event_id)

    def display_page(self):
        context = self.reset_context()
        context['event_categories'] = self.get_event_categories()
        context['published_events'] = self.get_events()
        context['registered_events'] = self.get_registered_events()

        return self.render_to_response(context)

    def unregister_for_event(self, event_id):
        reg = Registration.objects.get(user=self.request.user, event_id=event_id)
        reg.delete()
        return self.display_page()

    def register_for_event(self, event_id):
        reg = Registration(
            user=self.request.user,
            event=Event.objects.get(id=event_id),
        )
        reg.save()
        return self.display_page()

    def get_button_pressed(self, request):
        key = next(key for (key, value) in request.POST.iteritems() if ('register-' in key or 'unregister' in key))
        return key

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

    # TODO: If time conflict display warning
    # TODO: Allow user to remove badge associated with their account
    # TODO: Allow user to unregister from an event
    # TODO: Allow user to generate their event calendar
    # TODO: Limit based on published Conventions

    # - Maybe add filter for categories


register_redirect = RegisterRedirectView.as_view()
register_badge = RegisterBadgeView.as_view()
register_event = RegisterEventView.as_view()
