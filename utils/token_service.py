# utils/token_service.py

from datetime import timedelta

from django.db.models import Q

from core import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

User = get_user_model()


def generate_reset_password_token(user_info: str):
    """
    產生 JWT Token，僅用於忘記密碼驗證成功後的重設密碼流程。

    :param user_info: 使用者的手機號碼或信箱
    :return: JWT Token
    """
    try:
        user = User.objects.get(Q(phone=user_info) | Q(email=user_info))
    except User.DoesNotExist:
        return

    refresh = RefreshToken.for_user(user)
    refresh["reset_password"] = True  # 在 Payload 加上 reset_password 標記
    refresh.set_exp(lifetime=timedelta(minutes=settings.FORGET_PASSWORD_AUTH_TOKEN_EXPIRE_MINUTES))

    return str(refresh.access_token)


def decode_reset_password_token(token):
    """
    解碼 JWT Token 並取得對應的手機號碼。

    :param token: 忘記密碼時產生的 JWT Token
    :return: 驗證成功的手機號碼（若 Token 無效則回傳 None）
    """
    from rest_framework_simplejwt.tokens import AccessToken

    try:
        access_token = AccessToken(token)
        if access_token.get("reset_password") is True:
            return access_token["user_id"]  # `user_id` 是 SimpleJWT 預設存的 User PK
    except (TokenError, InvalidToken):
        return

    return
