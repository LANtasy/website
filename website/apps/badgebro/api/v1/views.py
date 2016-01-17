from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from website.apps.badgebro.api.v1 import serializers

logger = logging.getLogger(__name__)


class BadgeAuthenticateView(generics.GenericAPIView):

    serializer_class = serializers.BadgeAuthenticationSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        logger.info(self.request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            badge = serializer.validated_data['badge']
            badge_serializer = serializers.AuthenticatedBadgeSerializer(instance=badge)

            return Response(badge_serializer.data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid badge uid'}, status=status.HTTP_401_UNAUTHORIZED)


auth_badge = BadgeAuthenticateView.as_view()
