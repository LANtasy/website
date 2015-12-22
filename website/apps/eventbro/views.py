from braces.views import LoginRequiredMixin
from django.contrib.messages import error, warning
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView, RedirectView
from website.apps.badgebro.models import Badge
from website.apps.eventbro.forms import UpdateUserForm, UpdateBadgeForm
from website.apps.eventbro.models import Event, Registration


CHECKBOX_MAPPING = {'on': True, 'off': False, }


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
        if 'register' in request.POST:
            return self.register_for_event(event_id=self.kwargs['id'])
        elif 'unregister' in request.POST:
            return self.unregister_for_event(event_id=self.kwargs['id'])
        elif 'update' in request.POST:
            return self.update_event(event_id=self.kwargs['id'])
        else:
            # This should never occur
            return NotImplementedError

    def display_page(self):
        context = self.reset_context()
        context['event_categories'] = self.get_event_categories()
        context['published_events'] = self.modified_events()

        return self.render_to_response(context)

    def update_event(self, event_id):
        group = self.request.POST.get('group', None)
        game_id = self.request.POST.get('game_id', None)
        captain = self.request.POST.get('captain', 'off')
        captain = CHECKBOX_MAPPING.get(captain)
        try:
            reg = Registration.objects.get(user=self.request.user, event_id=event_id,)
            reg.group_name = group
            reg.group_captain = captain
            reg.game_id = game_id
            reg.save()
        except Registration.DoesNotExist:
            # Do Nothing - Registration doesn't exist, so can't update it
            pass
        url = reverse_lazy('eventbro:register_event')
        return HttpResponseRedirect(url)

    def unregister_for_event(self, event_id):
        try:
            reg = Registration.objects.get(user=self.request.user, event_id=event_id,)
            reg.delete()
        except Registration.DoesNotExist:
            # Do nothing, user is already unregistered
            pass
        url = reverse_lazy('eventbro:register_event')
        return HttpResponseRedirect(url)

    def register_for_event(self, event_id):
        event = Event.objects.get(id=event_id)
        # DO THIS BETTER
        group = self.request.POST.get('group', None)
        game_id = self.request.POST.get('game_id', None)
        captain = self.request.POST.get('captain', 'off')
        captain = CHECKBOX_MAPPING.get(captain)

        if event.is_full():
            warning(self.request, 'Event was full when registered, you have been waitlisted')
        try:
            Registration.objects.get(user=self.request.user, event_id=event_id,)
            # Do nothing since registration has already occured
        except Registration.DoesNotExist:
            reg = Registration(user=self.request.user, event_id=event_id,
                               group_name=group, game_id=game_id, group_captain=captain)
            reg.save()
        url = reverse_lazy('eventbro:register_event')
        return HttpResponseRedirect(url)

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

    def modified_events(self):
        events = self.get_events()
        modified_events = []
        for event in events:
            try:
                reg = Registration.objects.get(user=self.request.user, event_id=event.id,)
                event.registration = True
                event.group_name = reg.group_name
                event.group_captain = reg.group_captain
                event.game_id = reg.game_id
            except Registration.DoesNotExist:
                # Do nothing, registration doesn't exist
                pass
            modified_events.append(event)
        return modified_events

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

    @staticmethod
    def reset_context():
        context = {}
        return context

    # TODO: If time conflict display warning
    # TODO: Allow user to remove badge associated with their account
    # TODO: Allow user to generate their event calendar
    # TODO: Limit based on published Conventions

    # - Maybe add filter for categories


register_redirect = RegisterRedirectView.as_view()
register_badge = RegisterBadgeView.as_view()
register_event = RegisterEventView.as_view()
