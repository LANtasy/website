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
        parser.add_argument('-t', '--types', action='store_true', required=False, help='Fixes problems with badge types')
        # parser.add_argument('-q', '--qrcodes', action='store_true', required=False, help='Creates QR Codes')
        # parser.add_argument('-n', '--names', action='store_true', required=False, help='Sets all denormalized names')
        # parser.add_argument('-to', '--typeoptions', action='store_true', required=False, help='Sets all denormalized types and options')
        parser.add_argument('-a', '--all', action='store_true', required=False, help='Creates all types of objects')

    def handle(self, *args, **options):

        if options['all'] or options['types']:
            self.fix_badge_types()

    def fix_badge_types(self):
        """
        Fix any problems associated with type on badges
        """

        self.stdout.write("Fixing badge type problems...")

        queryset = Badge.objects.filter(type__isnull=False)

        for badge in queryset:
            if badge.type.endswith(' Pass'):
                badge.type = badge.type[:-5]
                badge.save()
