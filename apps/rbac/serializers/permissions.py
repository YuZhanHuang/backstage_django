from rest_framework import serializers
from ..models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S", help_text="建立時間")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S", help_text="更新時間")

    class Meta:
        model = Permission
        fields = ('id', 'code', 'description', 'is_active',
                  'category', 'updated_by', 'created_by', 'created_at', 'updated_at')


class PermissionActiveStatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)
