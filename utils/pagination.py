from django.utils.translation import gettext_lazy as _
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_description = _("分頁結果集中當前的頁碼")
    page_size_query_description = _("每頁返回的結果數量")

    def get_paginated_response(self, data):
        """
        自訂回應格式
        """
        return Response({
            "success": True,
            "message": "OK",
            "data": data,
            "meta": {
                "total_count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "page_size": self.get_page_size(self.request),
            }
        })


    def get_paginated_response_schema(self, schema):
        """
        覆寫 Swagger/OpenAPI 分頁回應的 Schema，符合 API 回應格式
        並增加 meta 欄位的詳細說明
        """
        return {
            "type": "object",
            "required": ["success", "data", "message", "meta"],
            "properties": {
                "success": {"type": "boolean", "example": True, "description": "請求是否成功"},
                "data": {"type": "array", "items": schema, "description": "分頁後的資料"},
                "message": {"type": "string", "example": "ok", "description": "API 回應訊息"},
                "meta": {
                    "type": "object",
                    "description": "分頁資訊",
                    "properties": {
                        "total_count": {"type": "integer", "example": 100, "description": "總共數量"},
                        "total_pages": {
                            "type": "integer",
                            "example": 10,
                            "description": "總頁數，依據 `page_size` 計算",
                        },
                        "current_page": {"type": "integer", "example": 1, "description": "目前所在的頁數"},
                        "page_size": {"type": "integer", "example": 10, "description": "每一頁顯示的數量"},
                    },
                },
            },
        }
