from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from common_models.utils.rules import validate_new_user_roles
from utils.mixins import GenericModelViewSet
from utils.response import GenericResponseMixin
from .filters import UserFilter
from .permissions import ActionPermission
from . import serializers
from . import openapi

User = get_user_model()


class AvatarViewSet(viewsets.ViewSet, GenericResponseMixin):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=serializers.AvatarSerializer,
        responses={200: {"message": "頭像更新成功"}},
        description="更新個人頭像"
    )
    @action(detail=False, methods=["patch"], url_path="avatar", url_name="avatar")
    def upload_avatar(self, request):
        """
        上傳頭像
        :param request:
        :return:
        """
        user = request.user
        serializer = serializers.AvatarSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "頭像更新成功"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(GenericModelViewSet):
    queryset = User.objects.prefetch_related('roles').filter(is_deleted=False).all()
    permission_classes = [IsAuthenticated, ActionPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == 'set_active_status':
            return serializers.UserActiveStatusSerializer
        if self.action in ['list', 'retrieve']:
            return serializers.UserSerializer
        return serializers.UserCreateUpdateSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        roles = serializer.validated_data.get('roles', [])
        validate_new_user_roles(creator, roles)
        serializer.save()

    def perform_update(self, serializer):
        creator = self.request.user
        roles = serializer.validated_data.get('roles', [])
        validate_new_user_roles(creator, roles)
        serializer.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance

    @openapi.user_list_schema
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @openapi.user_create_schema
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @openapi.user_update_schema
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @openapi.user_retrieve_schema
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @openapi.user_delete_schema
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @openapi.user_set_active_status_schema
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated, IsAdminUser])
    def set_active_status(self, request, pk=None):
        """
        設定使用者啟用狀態 (PATCH方法)
        """
        user = self.get_object()

        if user == request.user and not request.data.get('is_active', True):
            return self.format_response(
                data=[],
                message="無法禁用自己的帳號",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.is_active = serializer.validated_data['is_active']
        user.save()

        response_serializer = serializers.UserSerializer(user)
        return self.format_response(data=[response_serializer.data], message="使用者啟用狀態已更新")
