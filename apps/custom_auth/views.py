import uuid
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.custom_auth import serializers
from apps.custom_auth.serializers import ResetPasswordSerializer, ResetPasswordResponseSerializer, \
    CustomTokenObtainPairSerializer

User = get_user_model()


class LoginViewSet(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        request=serializers.LoginRequestSerializer,
        responses={200: serializers.LoginResponseSerializer},
        description="登入並取得 Access Token & Refresh Token",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                "success": True,
                "data": [{
                    "refresh": data["refresh"],
                    "access": data["access"],
                }],
                "message": "OK"
            }, status=200)
        # TODO 錯誤有關的議題，應交由全局的exception handler處理
        first_error = list(serializer.errors.values())[0][0]
        error_message = str(first_error)
        error_code = getattr(first_error, 'code', 401)

        return Response({
            "success": False,
            "message": error_message
        }, status=error_code if isinstance(error_code, int) else 401)


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=serializers.LogoutRequestSerializer,
        responses={200: serializers.LogoutResponseSerializer},
        description="登出並將 Refresh Token 加入黑名單",
    )
    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        """登出並將 Refresh Token 加入黑名單"""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # 將 Token 加入黑名單
            return Response({"message": "已成功登出", "success": True}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "無效的 Token", "success": False}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={
            200: ResetPasswordResponseSerializer,
            400: ResetPasswordSerializer,
        },
        description="重設密碼"
    )
    @action(detail=False, methods=["post"], url_path="reset_password")
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "密碼重設成功"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_unique_nickname():
    return slugify(f"user-{uuid.uuid4().hex[:45]}")
