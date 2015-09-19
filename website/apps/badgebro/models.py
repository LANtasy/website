import uuid

from django.conf import settings
from django.db import models

from cartridge.shop.models import Order
from website.apps.salesbro.models import TicketOption


class Badge(models.Model):

    # TODO: Will need m2m for registered events - this will actually go on the Event(s)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)

    order = models.ForeignKey(Order, related_name='badges')
    ticket = models.ForeignKey(TicketOption, related_name='badges')

    uid = models.CharField(max_length=34)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.uid:
            self.uid = self.generate_uid()

        return super(Badge, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{user}'.format(user=self.user_id)

    def generate_uid(self):
        return 'BA{uid}'.format(uid=uuid.uuid4().hex)

