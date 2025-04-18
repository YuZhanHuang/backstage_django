from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ViewSet

from apps.health.serializers import HealthCheckSerializer
from utils.throttles import CustomIPThrottle


class HealthCheckViewSet(ViewSet):
    """
    簡單的 Health Check API，只確認 Django 是否正常啟動
    """

    authentication_classes = []  # 不使用身份驗證
    permission_classes = [AllowAny]  # 允許任何人存取
    serializer_class = HealthCheckSerializer

    @extend_schema(responses={200: HealthCheckSerializer}, description="檢查 API 健康狀態")
    def list(self, request):
        return Response({"status": "OK"})
