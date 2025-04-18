from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.rbac import serializers, openapi
from utils.mixins import GenericModelViewSet
from ..models import Permission
from ..serializers.permissions import PermissionActiveStatusSerializer, PermissionSerializer


class PermissionViewSet(GenericModelViewSet):
    queryset = Permission.objects.all()  # noqa
    serializer_class = serializers.PermissionSerializer

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @openapi.permission_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @openapi.permission_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @openapi.permission_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @openapi.permission_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @openapi.permission_delete_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdminUser])
    def set_active_status(self, request, pk=None):
        permission = self.get_object()

        serializer = PermissionActiveStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        permission.is_active = serializer.validated_data['is_active']
        permission.updated_by = request.user
        permission.save()

        response_serializer = PermissionSerializer(permission)

        return Response({
            "success": True,
            "message": "權限啟用狀態已更新",
            "data": response_serializer.data
        }, status=status.HTTP_200_OK)
