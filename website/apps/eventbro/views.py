from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, RedirectView
from website.apps.badgebro.models import Badge
from website.apps.eventbro.forms import UpdateUserForm


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
        already_registered = self.check_badges_for_user()
        if already_registered:
            return HttpResponseRedirect(already_registered)
        else:
            return self.display_page()

    def display_page(self):
        context = self.reset_context()
        user_form = self.get_user_form()
        context['user_form'] = user_form
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
            'instance': self.request.user
        }
        return kwargs

    def get_user_form(self):
        kwargs = self.get_user_form_kwargs()
        form = UpdateUserForm(**kwargs)
        return form

    @staticmethod
    def reset_context():
        context = {}
        return context

    # - Explain that accurate firstname / lastname is required for picking up tickets at the door
    # - Show Firstname and lastname fields with the user's firstname and lastname entered, allow edit

    # - Show field for Badge ID, allow edit

    # - On click next
    #   - Look to see if Firstname/Lastname matches the logged in user, if not modify that record
    #   - Lookup badge
    #       - If invalid return to page with error
    #       - If valid save user to badge record, forward to EventReg


class RegisterEventView(LoginRequiredMixin, TemplateView):
    template_name = 'eventbro/registration/register_event.html'

    # TODO: Allow user to remove badge associated with their account
    # TODO: Allow user to unregister from an event
    # TODO: Allow user to generate their event calendar

    # - Lookup conventions that are published
    #   - Lookup events that are published associated with those conventions
    #       -Lookup if event is available for the associated badge
    #            -List all of the events that meet these criteria
    #                -If regular event, display register button, if full display waitlist button
    #                -if special event, display same as regular event, display additional required fields

register_redirect = RegisterRedirectView.as_view()
register_badge = RegisterBadgeView.as_view()
register_event = RegisterEventView.as_view()
