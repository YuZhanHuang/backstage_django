from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    success = serializers.BooleanField(default=False)


# class BaseResponseSerializer(serializers.Serializer):
#     """通用 API 響應格式"""
#     message = serializers.CharField(default="OK")
#     success = serializers.BooleanField(default=True)
#     data = serializers.SerializerMethodField()
#
#     def __init__(self, instance=None, data_class=None, many=False, **kwargs):
#         """允許 `data_class` 動態注入，支援 `many=True`"""
#         super().__init__(instance, **kwargs)
#         self.data_class = data_class
#         self.many = many
#
#     @extend_schema_field(serializers.ListField(child=serializers.DictField()))
#     def get_data(self, instance):
#         """使用 `data_class` 序列化 `data`"""
#         if not self.data_class:
#             return None  # 沒有提供 `data_class`，則 `data` 為 None
#
#         if self.many:
#             return self.data_class(instance, many=True).data  # 多筆資料
#         return self.data_class(instance).data  # 單筆資料

class BaseResponseSerializer(serializers.Serializer):
    """通用 API 響應格式"""
    message = serializers.CharField(default="OK")
    success = serializers.BooleanField(default=True)
    data = serializers.SerializerMethodField()

    def __init__(self, instance=None, data_class=None, **kwargs):
        """允許 `data_class` 動態注入，並確保 `data` 為 list"""
        super().__init__(instance, **kwargs)
        self.data_class = data_class

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_data(self, instance):
        """使用 `data_class` 序列化 `data`，確保 `data` 是 List"""
        if not self.data_class:
            return []

        return [self.data_class(instance).data]
