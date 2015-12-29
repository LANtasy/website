from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView


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
        # TODO: do de-reg

        return redirect('userbro:user_detail')

user_detail = UserDetailView.as_view()
user_release_badge = UserReleaseBadgeView.as_view()
