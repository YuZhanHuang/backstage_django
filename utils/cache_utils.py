from django.core.cache import cache
from apps.rbac.models import Role
from django.conf import settings


def _cache_key(role_id: int, user_type: str) -> str:
    return f"role:{role_id}:total_users:{user_type}"


def get_total_backstage_user(role_id: int, user_type: str) -> int:
    """
    Count & cache the total users of given type for this role.
    """
    key = _cache_key(role_id, user_type)
    count = cache.get(key)
    if count is None:
        count = (
            Role.objects
            .get(id=role_id)
            .users
            .filter(user_type=user_type)
            .count()
        )
        cache.set(key, count, timeout=600)
    return count


def update_total_role_users(role_id: int, user_type: str) -> None:
    """
    Force‐refresh the cache when role<->user assignments change.
    """
    key = _cache_key(role_id, user_type)
    count = (
        Role.objects
        .get(id=role_id)
        .users
        .filter(user_type=user_type)
        .count()
    )
    cache.set(key, count, timeout=600)


def get_fail_count(username):
    key = f"login_fail_{username}"
    return cache.get(key, 0)


def lock_account(username, timeout=None):
    if timeout is None:
        timeout = settings.LOGIN_LOCK_TIME
    cache.set(f"lock_{username}", True, timeout=timeout)


def increment_fail_count(username):
    key = f"login_fail_{username}"
    fail_count = cache.get(key, 0) + 1
    cache.set(key, fail_count, timeout=settings.LOGIN_FAIL_COUNT_TIMEOUT)
    return fail_count


def clear_fail_count(username):
    cache.delete(f"login_fail_{username}")


def is_account_locked(username):
    return cache.get(f"lock_{username}") is not None
