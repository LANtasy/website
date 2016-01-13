import uuid

from django.conf import settings
from django.db import models, transaction

from cartridge.shop.models import Order, OrderItem

from website.apps.salesbro.models import TicketOption


class BadgeGroup(object):

    VENDOR = 'vendor'
    TOURNAMENT = 'tournament'
    STAFF = 'staff'
    GENERAL = 'general'

    CHOCIES = (
        (VENDOR, 'Vendor'),
        (TOURNAMENT, 'Tournament'),
        (STAFF, 'Staff'),
        (GENERAL, 'General')
    )


class Badge(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True)

    # We don't necessarily need order/order items for a badge.
    # eg. Dobbo's badge would not have an order associated with it
    order = models.ForeignKey(Order, related_name='badge_order_id', blank=True, null=True)
    order_item = models.ForeignKey(OrderItem, related_name='badge_order_item', blank=True, null=True)

    ticket = models.ForeignKey(TicketOption, related_name='badges')

    uid = models.CharField(max_length=34, unique=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    type = models.CharField(max_length=20, default=BadgeGroup.GENERAL, choices=BadgeGroup.CHOCIES)

    # Need to add denormalized first/last name for the user onto the badge as
    # badges purchased at event may not have a user object to associate
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.uid:
            self.uid = self.generate_uid()

        return super(Badge, self).save(*args, **kwargs)

    def __unicode__(self):
        # return '{user}'.format(user=self.user_id)
        return '{uid}'.format(uid=self.uid)

    def generate_uid(self):
        return 'BA{uid}'.format(uid=uuid.uuid4().hex)

    def release(self):
        with transaction.atomic():
            self.user.registration_user.all().delete()
            self.user = None
            self.save()
