"""
backends.py

Custom authentication backend for Django that allows users to log in using their email address instead of a username.
This backend extends the default ModelBackend to authenticate users based on their email address.
This is useful for applications where users may not have a username or prefer to use their email for authentication.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user