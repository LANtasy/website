import logging

from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from website.apps.eventbro.models import Event

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


class EventForm(forms.Form):
    group_name = forms.CharField(label='Group/Team Name', max_length=255)
    game_id_name = forms.CharField(max_length=255)
    group_captain = forms.BooleanField(label='Are you the team captain?')

    class meta:
        fields = (
            'group_name',
            'game_id_name',
            'group_captain'
        )
