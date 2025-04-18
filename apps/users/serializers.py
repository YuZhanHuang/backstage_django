import hashlib
import os
from PIL import Image
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.rbac.serializers import RoleSerializer
from common_models.models.roles import Role
from utils.validators import validate_image_format, validate_username, \
    custom_password_validation

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        help_text="密碼",
    )
    roles = RoleSerializer(
        many=True,
        read_only=True,
        help_text="角色資料")

    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="名"
    )
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="姓"
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text="啟用狀態（true 啟用 / false 禁用）"
    )
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S", help_text="建立時間")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S", help_text="更新時間")

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'roles',
            'is_active',
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
        ]

    def get_created_by(self, obj):
        if obj.created_by:
            return {
                'id': obj.created_by.id,
                'username': obj.created_by.username
            }
        return '系統創建'

    def get_updated_by(self, obj):
        if obj.updated_by:
            return {
                'id': obj.updated_by.id,
                'username': obj.updated_by.username
            }
        return '系統創建'


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="帳號 (username 必填)"
    )
    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),  # noqa
        many=True
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        help_text="密碼",
    )
    first_name = serializers.CharField(
        required=True,
        allow_blank=True,
        help_text="名"
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=True,
        help_text="姓"
    )

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'first_name', 'last_name', 'roles', 'username']

    def validate_username(self, value):
        validate_username(value)
        return value

    def validate_password(self, value):
        custom_password_validation(value)
        validate_password(value, user=self.instance)
        return value

    def create(self, validated_data):
        roles = validated_data.pop('roles', [])
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.roles.set(roles)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        roles = validated_data.pop('roles', None)

        if password:
            instance.set_password(password)

        if roles is not None:
            instance.roles.set(roles)

        return super().update(instance, validated_data)


class UserActiveStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True, help_text="啟用狀態（true 啟用 / false 停用）")


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True, allow_empty_file=False, use_url=True)

    class Meta:
        model = User
        fields = ['avatar']

    def validate_avatar(self, avatar):
        """驗證圖片格式、尺寸、檔案大小"""
        validate_image_format(avatar)

        im = Image.open(avatar)
        if im.width != im.height:
            raise ValidationError("圖片必須是正方形。")

        # 檔案大小限制 2MB
        if avatar.size > 2 * 1024 * 1024:
            raise ValidationError("圖片大小不可超過 2MB。")

        return avatar

    def update(self, instance, validated_data):
        avatar = validated_data.get("avatar")

        if avatar:
            # 計算 SHA256 哈希值，確保檔案名稱唯一
            file_hash = hashlib.sha256(avatar.read()).hexdigest()
            file_ext = os.path.splitext(avatar.name)[-1]  # 保留原始副檔名 (如 .jpg, .png)
            avatar_name = f"{file_hash}{file_ext}"

            # 重置讀取指標，避免文件內容被消耗
            avatar.seek(0)

            with transaction.atomic():
                # 儲存帶有哈希名稱的檔案
                instance.avatar.save(f"{avatar_name}", avatar, save=False)
                instance.save(update_fields=["avatar"])

                # 在 transaction 提交後產生縮圖
                transaction.on_commit(lambda: self.generate_thumbnail(instance))

        return instance

    def generate_thumbnail(self, user):
        from apps.users.tasks import generate_avatar_thumbnail
        generate_avatar_thumbnail.delay(user.pk)


class SuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="成功", help_text="成功訊息")


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text="錯誤訊息")


class FrontstageUserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)
    # avatar = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), allow_null=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'nickname',
            'phone',
            'email',
            'address',
            'birthday',
            'avatar',
            'avatar_url',
            'identity_no',
            'last_edited_by',
            'last_login_at',
            'mcoin',
            'region',
            'invite_code',
            'referrer',
            'member_level',
            'member_type',
            'is_active',
            'is_staff',
            'is_email_verified',
            'is_phone_verified',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'last_edited_by',
            'last_login_at',
            'mcoin',
            'is_staff',
            'is_email_verified',
            'is_phone_verified',
            'date_joined',
            'avatar_url',
        ]

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and obj.avatar.file:
            return request.build_absolute_uri(obj.avatar.file.url) if request else obj.avatar.file.url
        return None
