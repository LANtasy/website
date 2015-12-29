import logging

from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory


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


class IndividualEventRegistrationForm(forms.Form):
    """
    Registers a user for an event
    """
    game_id_name = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event')
        super(IndividualEventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['game_id_name'].required = self.event.require_game_id

    def save(self, user):
        game_id = self.cleaned_data.get('game_id_name')
        registrant = self.event.register(user=user, game_id=game_id)
        return registrant


class GroupEventRegistrationForm(IndividualEventRegistrationForm):
    """
    Registers a group for an event
    """

    group_name = forms.CharField(label='Group/Team Name', max_length=255)
    group_captain = forms.BooleanField(label='Are you the team captain?', required=False)

    def __init__(self, *args, **kwargs):
        super(GroupEventRegistrationForm, self).__init__(*args, **kwargs)

    def save(self, user):
        group_name = self.cleaned_data.get('group_name')
        game_id = self.cleaned_data.get('game_id_name')
        is_captain = self.cleaned_data.get('group_captain')
        registrant = self.event.register(user=user, group=group_name, game_id=game_id, is_captain=is_captain)
        return registrant
