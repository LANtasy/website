from __future__ import unicode_literals
import logging
import datetime
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils import timezone

from website.apps.badgebro.models import Badge
from website.apps.salesbro.models import TicketOption

User = get_user_model()


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'backfills with extra users, message types etc'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--qrcodes', action='store_true', required=False, help='Creates QR Codes')
        parser.add_argument('-n', '--names', action='store_true', required=False, help='Sets all denormalized names')
        parser.add_argument('-to', '--typeoptions', action='store_true', required=False, help='Sets all denormalized types and options')
        parser.add_argument('-a', '--all', action='store_true', required=False, help='Creates all types of objects')

    def handle(self, *args, **options):

        if options['all'] or options['qrcodes']:
            self.setup_badge_qrcodes()

        if options['all'] or options['names']:
            self.setup_badge_names()

        if options['all'] or options['typeoptions']:
            self.setup_badge_typeoption()

    def setup_badge_qrcodes(self):
        """
        Generate all the QR codes for badges that do not yet have a QR code
        """

        self.stdout.write("Generating badge QR codes...")

        queryset = Badge.objects.filter(qr_code__isnull=True)

        for badge in queryset:
            badge.create_qr_code()

    def setup_badge_names(self):
        """
        Set the denormalized badge names to the claimed users name or the ordering users name.
        """

        self.stdout.write("Setting badge names...")

        queryset = Badge.objects.select_related('user', 'order').all()

        for badge in queryset:

            # Skip over badges that already have names
            if badge.first_name or badge.last_name:
                continue

            if badge.user:
                badge.first_name = badge.user.first_name
                badge.last_name = badge.user.last_name

            elif badge.order:
                badge.first_name = badge.order.billing_detail_first_name
                badge.last_name = badge.order.billing_detail_last_name

            badge.save()

    def setup_badge_typeoption(self):
        """
        Set the denormalized badge type and option to the associated Ticket and TicketOption values
        """

        self.stdout.write("Setting badge types/options...")

        queryset = Badge.objects.select_related('ticket').all()

        for badge in queryset:

            badge.option = badge.ticket.ticket.title

            if badge.ticket.title.endswith(' Pass'):
                badge.type = badge.ticket.title[:-5]
            else:
                badge.type = badge.ticket.title

            badge.save()


