# -*- coding: utf-8 -*-
# Author:wrd
from django.contrib.auth.backends import ModelBackend


class MyRemoteUserBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?

    def authenticate(self, pk, token):
        try:
            from django.contrib.auth import get_user_model
        except ImportError:  # Django < 1.5
            from django.contrib.auth.models import User
        else:
            User = get_user_model()
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

        if not user.is_active:
            return None
        from common.views import check_token
        if check_token(pk,token):
            return user
        return None
