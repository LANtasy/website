from braces.views import LoginRequiredMixin
from django.contrib.messages import info
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView, FormView, TemplateView
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.urls import login_redirect

from website.apps.badgebro.models import Badge
from website.apps.eventbro.models import Registration, Convention
from website.apps.userbro.forms import LoginForm


class UserView(object):
    queryset = User.objects.filter(is_active=True)

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(LoginRequiredMixin, SuccessMessageMixin, UserView, UpdateView):

    template_name = 'userbro/user_detail.html'
    success_message = 'Successfully updated profile'
    success_url = reverse_lazy('userbro:user_detail')
    fields = (
        'first_name',
        'last_name',
        'email',
    )


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, UserView, FormView):
    template_name = 'userbro/change_password.html'
    form_class = PasswordChangeForm
    success_message = 'Successfully changed password'
    success_url = reverse_lazy('userbro:user_detail')

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.get_object(), **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one if
        # django.contrib.auth.middleware.SessionAuthenticationMiddleware
        # is enabled.
        update_session_auth_hash(self.request, form.user)
        return HttpResponseRedirect(self.get_success_url())


class UserReleaseBadgeView(LoginRequiredMixin, SuccessMessageMixin, UserView, DetailView):
    template_name = 'userbro/user_badge_release.html'
    success_message = 'Successfully released badge'

    def post(self, request, *args, **kwargs):
        try:
            badge = Badge.objects.get(user=self.get_object())
            badge.release()
        except Badge.DoesNotExist:
            # Do nothing
            pass

        return redirect('userbro:user_detail')


class UserScheduleView(LoginRequiredMixin, TemplateView):
    success_message = 'Successfully printed schedule'

    # On view page there should be a printer friendly button
    #  - Button will set some url or session key or flag
    # Both pages use schedule_detail.html to display the schedule

    def get_template_names(self):
        if self.is_printer_friendly():
            return ['userbro/schedule/print_schedule.html']
        else:
            return ['userbro/schedule/view_schedule.html']

    def get_context_data(self, **kwargs):
        registrations = Registration.objects.filter(user=self.request.user)
        registrations = registrations.order_by('event__start')
        kwargs['registrations'] = registrations
        kwargs['convention'] = Convention.objects.get(active=True)
        return kwargs

    def is_printer_friendly(self):
        try:
            action = self.kwargs['action']
        except KeyError:
            return False

        if action == 'print':
            return True
        else:
            return False


def login(request, template="accounts/account_login.html", extra_context=None):
    """
    Login form.
    """
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        authenticated_user = form.save()
        info(request, _("Successfully logged in"))
        auth_login(request, authenticated_user)
        return login_redirect(request)

    context = {"form": form, "title": _("Log in")}
    context.update(extra_context or {})
    return render(request, template, context)

user_detail = UserDetailView.as_view()
user_release_badge = UserReleaseBadgeView.as_view()
change_password = ChangePasswordView.as_view()
schedule = UserScheduleView.as_view()
