from __future__ import unicode_literals, absolute_import

import logging

from django import forms

from website.apps.badgebro.models import Badge, PaymentMethod
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


class BadgeUpdateForm(forms.ModelForm):

    option = forms.ChoiceField(choices=(), required=True)
    type = forms.ChoiceField(choices=(), required=True)

    class Meta:
        model = Badge
        fields = ('first_name', 'last_name', 'network', 'option', 'type')

    def __init__(self, *args, **kwargs):
        super(BadgeUpdateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['option'].choices = self.get_option_choices()
        self.fields['type'].choices = self.get_type_choices()

    def get_type_choices(self):
        """
        Get the choices for the badge option
        """
        STAFF = 'staff'
        VENDOR = 'vendor'

        choices = [
            (STAFF, STAFF.title()),
            (VENDOR, VENDOR.title()),
        ]

        option_choices = Badge.objects.type_choices()

        for choice in option_choices:
            if choice == STAFF or choice == VENDOR:
                continue

            choices.append((choice, choice.title()))

        return choices

    def get_option_choices(self):
        """
        Get the choices for the badge type
        """

        choices = []

        option_choices = Badge.objects.option_choices()

        for choice in option_choices:

            choices.append((choice, choice.title()))

        return choices


class BadgeUpgradeForm(forms.ModelForm):

    new_ticket_option = forms.ModelChoiceField(queryset=TicketOption.objects.none(), label='New')
    payment_method = forms.ChoiceField(choices=PaymentMethod.CHOICES)

    class Meta:
        model = Badge
        fields = ('new_ticket_option', )

    def __init__(self, *args, **kwargs):
        super(BadgeUpgradeForm, self).__init__(*args, **kwargs)

        if self.instance is not None:
            self.fields['new_ticket_option'].queryset = self.instance.ticket.upgradeable_to()
