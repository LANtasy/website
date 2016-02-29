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
        parser.add_argument('-u', '--users', required=False, type=int, help='Creates n users')
        parser.add_argument('-b', '--badges', required=False, help='Creates badges')
        parser.add_argument('-a', '--all', required=False, type=int, help='Creates all types of objects')

    def handle(self, *args, **options):

        if options['all'] or options['users']:
            self.create_test_users(options['users'])
        if options['all'] or options['badges']:
            self.create_test_badges()

    def create_test_users(self, number_of_new_users=10):
        """
        create n or 10 users
        :return:
        """

        WORDS = self.get_words()

        count = User.objects.count()

        for i in range(count, count + number_of_new_users):

            first_name = random.choice(WORDS).title()
            last_name = random.choice(WORDS).title()

            try:
                user = User()
                user.username = '%s.%s' % (first_name, last_name)
                user.first_name = first_name
                user.last_name = last_name

                user.email = '%s.%s@lantasy.com' % (first_name, last_name)

                user.last_login = timezone.now()
                user.is_superuser = False
                user.is_staff = False
                user.set_password('iliketotoot')

                user.save()
            except IntegrityError:
                self.stdout.write(user.username + 'already exists, skipping')

    def create_test_badges(self):

        tickets = TicketOption.objects.values_list('id', flat=True)

        for user in User.objects.all():

            try:
                badge = Badge.objects.get(user=user)
            except Badge.DoesNotExist:
                badge = Badge()

                badge.ticket_id = random.choice(tickets)
                badge.user = user
                badge.first_name = user.first_name
                badge.last_name = user.last_name
                badge.save()


    def get_words(self):
        import requests
        word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = requests.get(word_site)
        WORDS = response.content.splitlines()
        return WORDS
