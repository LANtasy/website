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


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'image', 'name',
            'start', 'end',
            'description',
        )

EventFormSet = modelformset_factory(Event, form=EventForm, extra=0, can_delete=False, can_order=True,)
