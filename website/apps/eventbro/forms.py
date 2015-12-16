import logging

from django import forms
from django.contrib.auth.models import User
from website.apps.badgebro.models import Badge

logger = logging.getLogger(__name__)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class UpdateBadgeForm(forms.Form):
    uid = forms.CharField(label='UID', max_length=34)

    class Meta:
        fields = (
            'uid',
        )
