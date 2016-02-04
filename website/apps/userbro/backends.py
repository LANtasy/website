from __future__ import unicode_literals, absolute_import

import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import base36_to_int
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend as DefaultModelBackend

logger = logging.getLogger(__name__)

User = get_user_model()


class AuthenticationBackend(DefaultModelBackend):

    def authenticate(self, **kwargs):
        if kwargs:
            username = kwargs.pop("username", None)
            if username:
                username_or_email = Q(username__iexact=username) | Q(email__iexact=username)
                password = kwargs.pop("password", None)
                try:
                    user = User.objects.get(username_or_email, **kwargs)
                    if user.check_password(password):
                        return user
                except User.DoesNotExist:
                    # Run the default password hasher once to reduce the timing
                    # difference between an existing and a non-existing user (#20760).
                    User().set_password(password)
                except User.MultipleObjectsReturned:
                    # Run the default password hasher once to reduce the timing
                    # difference between an existing and a non-existing user (#20760).
                    User().set_password(password)
                    logger.error("Duplicate username: %s", username)
            else:
                if 'uidb36' not in kwargs:
                    return
                kwargs["id"] = base36_to_int(kwargs.pop("uidb36"))
                token = kwargs.pop("token")
                try:
                    user = User.objects.get(**kwargs)
                except User.DoesNotExist:
                    pass
                else:
                    if default_token_generator.check_token(user, token):
                        return user
