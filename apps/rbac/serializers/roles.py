from rest_framework import serializers

from common_models.common.constant import UserType
from .permissions import PermissionSerializer
from ..models import Role, Permission
from utils.cache_utils import get_total_backstage_user as total_backstage_users


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S", help_text="建立時間")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S", help_text="更新時間")
    # total_backstage_users = serializers.SerializerMethodField()
    total_backstage_users = serializers.IntegerField(read_only=True)
    total_frontstage_users = serializers.IntegerField(read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'level', 'permissions',
                  'updated_by', 'created_by',
                  'updated_at', 'created_at',
                  'is_active',
                  'total_backstage_users', 'total_frontstage_users'
                  ]

    # def get_total_backstage_users(self, obj):
    #     return total_backstage_users(obj.id, UserType.BACK)  # 使用快取取得總數


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),  # noqa
        many=True,
        help_text="請提供permission的id"
    )
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Role
        fields = ['id', 'name', 'level', 'permissions', 'updated_by', 'created_by']


class RoleActiveStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()
