from __future__ import absolute_import, unicode_literals

import csv
import logging
from dateutil import parser

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from website.apps.eventbro.models import Registration, Event, Convention, EventType, Sponsor
from website.apps.salesbro.models import TicketOption

logger = logging.getLogger(__name__)


class DateAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(DateAdminForm, self).clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start > end:
            msg = 'Start date must be before End date'
            self.add_error('start', msg)
            self.add_error('end', msg)


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


class RegistrationUpdateForm(forms.ModelForm):

    class Meta:
        model = Registration

        fields = (
            'group_name',
            'game_id',
            'group_captain',
        )

    def __init__(self, *args, **kwargs):
        super(RegistrationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['game_id'].required = self.instance.event.require_game_id
        self.fields['group_name'].required = self.instance.event.group_event


class EventImportForm(forms.Form):

    events = None
    ticket_types = None
    event_types = None
    sponsors = None
    convention = None

    required_fields = (
        'name',
        'start',
        'end',
        'size',
        'type',
        'organizer',
    )

    optional_fields = (
        'ticket types',
        'description',
        'published',
        'require game id',
        'game id',
        'sponsor',
        'prizes',
        'rules',
    )

    event_csv = forms.FileField(required=True)

    def clean(self):
        csv_file = self.cleaned_data['event_csv']
        events = self.parse_csv(csv_file)

        self.events = events

    def save(self):

        for event in self.events:
            event.save()
            event.valid_options = event.ticket_types

        return self.events

    def get_ticket_types(self):
        self.ticket_types = {}
        ticket_option_queryset = TicketOption.objects.all()
        self.ticket_types = {ticket_option.id: ticket_option for ticket_option in ticket_option_queryset}

    def get_event_types(self):
        event_types_queryset = EventType.objects.all()

        self.event_types = {event_type.name: event_type for event_type in event_types_queryset}

    def get_sponsors(self):
        sponsor_queryset = Sponsor.objects.filter(convention=self.convention)

        self.sponsors = {sponsor.name: sponsor for sponsor in sponsor_queryset}

    def parse_csv(self, csv_file):
        """
        Parses the csv into a list of dictionaries
        """

        convention = Convention.objects.get_active_convention()

        self.convention = convention

        self.get_ticket_types()
        self.get_event_types()

        if not convention:
            raise ValidationError("Could not find active Convention")

        reader = csv.DictReader(csv_file)

        for field in self.required_fields:
            if field not in reader.fieldnames:
                message = 'Missing required field: %s' % field
                raise ValidationError(message)

        events = []

        for index, row in enumerate(reader):

            for field in self.required_fields:

                value = row.get(field)

                if not value:
                    message = 'Missing value for required field %s on row %s' % (field, index+2)
                    raise ValidationError(message)

            if row['type'] not in self.event_types:
                message = "Event Type %s on row %s not found" % (row['type'], index+2)
                raise ValidationError(message)

            event_start = self.string_to_datetime(row['start'])
            event_end = self.string_to_datetime(row['end'])

            event = Event()
            event.name = row['name']
            event.size = row['size']
            event.organizer = row['organizer']
            event.prizes = row.get('prizes', '')
            event.rules = row.get('rules', '')
            event.event_type = self.event_types[row['type']]
            event.start = event_start
            event.end = event_end
            event.convention = convention
            event.ticket_types = []

            if row.get('sponsor'):
                event.sponsor = self.sponsors.get(row['sponsor'])

            try:
                description = row.get('description', '').encode('utf8')
                encoded_desc = unicode(description, errors='ignore')
                event.description = encoded_desc
            except UnicodeDecodeError:
                message = 'Invalid character encoding detected in description on line %s' % (index + 2, )
                raise ValidationError(message)

            if 'ticket types' in reader.fieldnames:

                ticket_type_ids = map(int, row['ticket types'].split(','))

                for ticket_type_id in ticket_type_ids:
                    try:
                        ticket_type = self.ticket_types[ticket_type_id]
                    except KeyError:
                        message = "Invalid ticket type %s on row %s" % (ticket_type_id, index+2)
                        raise ValidationError(message)

                    event.ticket_types.append(ticket_type)

            events.append(event)

        return events

    def string_to_datetime(self, date_string, tz=None):
        try:
            dt = parser.parse(date_string)
        except ValueError:
            raise ValidationError("Invalid date time detected: %s" % date_string)

        dt = timezone.make_aware(dt, timezone=tz)

        return dt
