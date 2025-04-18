from django.db.models import Count, Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.rbac import serializers, openapi
from common_models.common.constant import UserType
from utils.cache_utils import update_total_role_users
from utils.mixins import GenericModelViewSet
from utils.pagination import StandardResultsSetPagination
from utils.response import format_paginated_response
from ..models import Role
from ...users.serializers import UserSerializer


class RoleViewSet(GenericModelViewSet):
    queryset = (
        Role.objects
        .prefetch_related("permissions")
        .annotate(
            total_backstage_users=Count(
                "users",
                filter=Q(users__user_type=UserType.BACK),
                distinct=True
            ),
            total_frontstage_users=Count(
                "users",
                filter=Q(users__user_type=UserType.FRONT),
                distinct=True
            ),
        )
    )
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'set_active_status':
            return serializers.RoleActiveStatusSerializer
        if self.action in ['list', 'retrieve']:
            return serializers.RoleSerializer
        return serializers.RoleCreateUpdateSerializer

    def perform_create(self, serializer):
        role = serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )
        update_total_role_users(role.id, UserType.BACK)

    def perform_update(self, serializer):
        role = serializer.save(updated_by=self.request.user)
        update_total_role_users(role.id, UserType.BACK)

    @openapi.role_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @openapi.role_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @openapi.role_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @openapi.role_update_schema
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(
        detail=True, methods=['get'], url_path='backstage_users',
        pagination_class=StandardResultsSetPagination,
    )
    def users(self, request, pk=None):
        """
        取得該角色的後台使用者，支援 **分頁** 與 **搜尋**
        """
        role = self.get_object()
        qs = role.users.all()
        t = request.query_params.get("user_type")
        if t in (UserType.FRONT, UserType.BACK):
            qs = qs.filter(user_type=t)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return format_paginated_response([], request, paginator=self.paginator)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdminUser])
    def set_active_status(self, request, pk=None):
        role = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role.is_active = serializer.validated_data['is_active']
        role.updated_by = request.user
        role.save()

        response_serializer = serializers.RoleSerializer(role)

        # FIXME
        from rest_framework.response import Response
        from rest_framework import status
        return Response({
            "success": True,
            "message": "角色啟用狀態已更新",
            "data": response_serializer.data
        }, status=status.HTTP_200_OK)
