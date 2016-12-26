# Taken from http://stackoverflow.com/questions/6560182/django-authentication-without-a-password

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class PasswordlessAuthBackend(ModelBackend):
    """Log in to Django without providing a password."""

    def authenticate(self, email=None, active=True):
        try:
            return User.objects.get(email=email, is_active=active)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
