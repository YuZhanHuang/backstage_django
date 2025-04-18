from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

from core.exceptions.exceptions import InvalidCredentials, AccountDisabled, AccountLocked
from utils.cache_utils import (
    lock_account,
    increment_fail_count,
    clear_fail_count,
    is_account_locked,
)

User = get_user_model()


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            raise InvalidCredentials()

        user = None
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(Q(email=username) | Q(phone=username))

            if not user.is_active:
                raise AccountDisabled()

            if user.check_password(password):
                clear_fail_count(username)
                return user

        except User.DoesNotExist:
            pass

        fail_count = increment_fail_count(username)

        if fail_count >= settings.PERMANENT_LOCK_THRESHOLD:
            if user:
                user.is_active = False
                user.save()
            clear_fail_count(username)
            raise AccountDisabled()

        if fail_count % settings.TEMP_LOCK_THRESHOLD == 0:
            lock_account(username)
            raise AccountLocked()

        if is_account_locked(username):
            raise AccountLocked()

        raise InvalidCredentials()

