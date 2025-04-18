from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from rest_framework import status, serializers
from rest_framework.response import Response


def format_paginated_response(data, request, paginator):
    """
    格式化分頁回應，確保當資料為空時，仍然有 `meta` 欄位
    """
    return Response({
        "success": True,
        "message": "OK",
        "data": data,
        "meta": {
            "total_count": paginator.page.paginator.count if paginator.page.paginator.count else 0,
            "total_pages": paginator.page.paginator.num_pages if paginator.page.paginator.num_pages else 0,
            "current_page": paginator.page.number if paginator.page.number else 1,
            "page_size": paginator.get_page_size(request),
        }
    })


class GenericResponseMixin:
    def format_response(self, success=True, message="OK", data=None, status_code=status.HTTP_200_OK):
        return Response({"success": success, "message": message, "data": data}, status=status_code)


def generic_success_response(data_serializer_class, example=None, *args, **kwargs):
    method = kwargs.get('method', 'Magic')

    serializer_name = f"Generic{data_serializer_class.__name__}{method}Response"
    generic_serializer = serializers.ListSerializer(child=data_serializer_class())

    example = example or [{"id": 1}]
    val = {
        'success': True,
        'message': 'OK',
        'data': example,
        'meta': {
            'total_count': 19,
            'total_page': 2,
            'current_page': 1,
            'page_size': 10
        }
    }

    return OpenApiResponse(
        response=generic_serializer,
        description="統一成功回應 (純陣列)",
        examples=[
            OpenApiExample(
                name=f"{serializer_name}Example",
                value=val
            )
        ]
    )
