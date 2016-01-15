from __future__ import unicode_literals, absolute_import

import logging

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext

logger = logging.getLogger(__name__)

from mezzanine.accounts.forms import LoginForm as MezLoginForm


class LoginForm(MezLoginForm):

    def clean(self):
        """
        Authenticate the given username/email and password. If the fields
        are valid, store the authenticated user for returning via save().
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError(
                             ugettext("Invalid username/email and password"))
        elif not self._user.is_active:
            raise forms.ValidationError(ugettext("Your account has not yet been activated."))
        return self.cleaned_data
