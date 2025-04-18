from rest_framework import serializers


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="API 健康狀態，固定回傳 'ok'")
