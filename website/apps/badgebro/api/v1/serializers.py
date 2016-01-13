from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from website.apps.badgebro.models import Badge

logger = logging.getLogger(__name__)


class BadgeAuthenticationSerializer(serializers.Serializer):

    badge_uid = serializers.CharField(min_length=12, max_length=12, required=True)

    def validate(self, attrs):

        logger.debug("Finding badge with uid ending in: %s", attrs['badge_uid'])
        badge = Badge.objects.filter(uid__iendswith=attrs['badge_uid']).first()

        if not badge:
            raise ValidationError("Invalid Badge Id")

        attrs['badge'] = badge

        return attrs


class AuthenticatedBadgeSerializer(serializers.Serializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    type = serializers.CharField()
