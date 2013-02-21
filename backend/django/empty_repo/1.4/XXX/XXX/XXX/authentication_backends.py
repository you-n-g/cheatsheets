from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend

class SettingsBackends(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            setting_password = settings.AUTHENTICATION_PASSWORD
        except AttributeError:
            return None

        is_valid = (password == setting_password) or (isinstance(setting_password, list) and (password in setting_password))
        try:
            user = User.objects.get(username=username)
            if is_valid:
                return user
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.get(email=username)
            if is_valid:
                return user
        except User.DoesNotExist:
            pass

        return None

class EmailModelBackend(object):
    def authenticate(self, username=None, password=None):
        kwargs = {'email': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
