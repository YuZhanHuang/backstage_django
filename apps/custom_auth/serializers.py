from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers
from core.exceptions.exceptions import (
    AccountLocked, AccountDisabled, InvalidCredentials
)
from utils.validators import validate_phone, validate_password_complexity

User = get_user_model()


class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        help_text="使用者名稱"
    )
    password = serializers.CharField(help_text="用戶的密碼", write_only=True)


class TokenDataSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="JWT Access Token")
    refresh = serializers.CharField(help_text="JWT Refresh Token")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get("password")

        try:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password
            )

            if not user:
                raise InvalidCredentials()

            data = super().get_token(user)
            return {
                "refresh": str(data),
                "access": str(data.access_token),  # noqa
                "user_id": user.id,
                "username": user.username,
            }

        except (AccountLocked, AccountDisabled, InvalidCredentials) as exc:
            raise serializers.ValidationError(exc.default_detail, code=exc.status_code)


class LoginResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    data = serializers.ListField(child=TokenDataSerializer())  # 這裡明確定義 data 的內容
    message = serializers.CharField(default="OK")


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="JWT 的 Refresh Token")


class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="登出結果訊息，例如 '已成功登出' 或 '無效的 Token'")
    success = serializers.BooleanField(help_text="登出是否成功，`true` 表示成功，`false` 表示失敗")


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=20,
        help_text=_("密碼必須包含大小寫字母、數字，長度8-20個字元")
    )
    confirm_password = serializers.CharField(
        write_only=True,
        help_text=_("請再次輸入密碼，需與新密碼一致")
    )

    def validate_new_password(self, value):
        # 呼叫通用密碼驗證函式，允許調整規則
        validate_password_complexity(
            password=value,
            min_length=8,
            max_length=20,
            require_upper=True,
            require_lower=True,
            require_digit=True,
            require_special=False,
            special_chars="._-",
            forbid_spaces=True,  # 允許調整是否禁止空格
            forbid_fullwidth=True  # 允許調整是否禁止全形字元
        )

        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        user = self.context["request"].user

        if user.check_password(new_password):
            raise serializers.ValidationError({"new_password": _("新密碼不能與之前的密碼相同")})

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": _("兩次密碼輸入不一致")})

        return attrs

    def save(self):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()


class ResetPasswordResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="密碼重設成功")
