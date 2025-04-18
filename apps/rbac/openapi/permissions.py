from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from ..serializers import PermissionSerializer
from utils.response import generic_success_response

permission_list_schema = extend_schema(
    summary="取得權限列表",
    description="取得所有權限的列表，可以透過分類（category）進行過濾。",
    parameters=[
        OpenApiParameter(
            name='category',
            description='權限分類過濾條件，例如：category=user',
            type=str,
            required=False,
            examples=[
                OpenApiExample('Category Example', value='user')
            ]
        ),
    ],
    responses={
        200: generic_success_response(
            PermissionSerializer,
            method="List",
            example=[
                {
                    "id": 1,
                    "code": "user:add",
                    "description": "新增使用者",
                    "category": "user"
                }
            ]
        )
    }
)

permission_create_schema = extend_schema(
    summary="新增權限",
    description="新增一個新的權限項目，須指定 code、description 與 category。",
    request=PermissionSerializer,
    responses={
        201: generic_success_response(
            PermissionSerializer,
            method="Create",
            example=[{
                "id": 2,
                "code": "user:delete",
                "description": "刪除使用者",
                "category": "user"
            }]
        )
    }
)

permission_retrieve_schema = extend_schema(
    summary="取得單一權限詳情",
    description="透過權限 ID 取得該權限的詳細資料。",
    responses={
        200: generic_success_response(
            PermissionSerializer,
            method="Retrieve",
            example=[{
                "id": 1,
                "code": "user:add",
                "description": "新增使用者",
                "category": "user"
            }]
        ),
        404: OpenApiResponse(description="權限不存在"),
    }
)

permission_update_schema = extend_schema(
    summary="更新權限",
    description="根據權限 ID 更新權限資訊。",
    request=PermissionSerializer,
    responses={
        200: generic_success_response(
            PermissionSerializer,
            method="Update",
            example=[{
                "id": 1,
                "code": "user:update",
                "description": "更新使用者資料",
                "category": "user"
            }]
        ),
        400: OpenApiResponse(description="請求格式錯誤"),
        404: OpenApiResponse(description="權限不存在"),
    }
)

permission_delete_schema = extend_schema(
    summary="刪除權限",
    description="根據權限 ID 刪除該權限。",
    responses={
        204: OpenApiResponse(description="權限刪除成功（無回傳內容）"),
        404: OpenApiResponse(description="權限不存在"),
    }
)
