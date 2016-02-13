from __future__ import unicode_literals, absolute_import

import logging

from django import forms

from website.apps.badgebro.models import Badge, PaymentMethod
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


class BadgeUpdateForm(forms.ModelForm):

    class Meta:
        model = Badge
        fields = ('first_name', 'last_name', 'type', )

    def __init__(self, *args, **kwargs):
        super(BadgeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


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
