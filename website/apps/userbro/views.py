from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView
from website.apps.badgebro.models import Badge
from website.apps.eventbro.models import Registration


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


class UserReleaseBadgeView(LoginRequiredMixin, SuccessMessageMixin, UserView, DetailView):
    template_name = 'userbro/user_badge_release.html'
    success_message = 'Successfully released badge'

    def post(self, request, *args, **kwargs):
        user = self.request.user
        self.remove_badge_association(user=user)
        self.remove_registrations(user=user)

        return redirect('userbro:user_detail')

    @staticmethod
    def remove_badge_association(user):
        try:
            badge = Badge.objects.get(user=user)
            badge.user = None
            badge.save()
        except Badge.DoesNotExist:
            pass

    @staticmethod
    def remove_registrations(user):
        try:
            registrations = Registration.objects.get(user=user)
        except Registration.DoesNotExist:
            registrations = None

        for registration in registrations:
            try:
                registration.delete()
            except Registration.DoesNotExist:
                pass

user_detail = UserDetailView.as_view()
user_release_badge = UserReleaseBadgeView.as_view()
