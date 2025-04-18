from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from ..serializers import RoleSerializer, RoleCreateUpdateSerializer
from utils.response import generic_success_response

role_list_schema = extend_schema(
    summary="取得角色列表",
    description="取得角色的完整列表，可以透過層級（level）進行過濾。",
    parameters=[
        OpenApiParameter(
            name='level',
            description='角色層級過濾條件，例如：level=3，數字越小權限越高',
            type=int,
            required=False,
            examples=[
                OpenApiExample('Level Example', value=3)
            ]
        ),
    ],
    responses={
        200: generic_success_response(
            RoleSerializer,
            paginated=True,
            method="List",
            example=[
                {
                    "id": 1,
                    "name": "Admin",
                    "level": 1,
                    "permissions": [
                        {"id": 1, "code": "orders:view", "description": "查看訂單"}
                    ]
                }
            ]
        )
    }
)

role_create_schema = extend_schema(
    summary="新增角色",
    description="新增一個角色並指定相關權限。",
    request=RoleCreateUpdateSerializer,
    responses={
        201: generic_success_response(
            RoleSerializer,
            method="Create",
            example=[{
                "id": 2,
                "name": "Staff",
                "level": 3,
                "permissions": [
                    {"id": 1, "code": "orders:view", "description": "查看訂單"},
                    {"id": 2, "code": "orders:edit", "description": "編輯訂單"}
                ]
            }]
        )
    },
)

role_retrieve_schema = extend_schema(
    summary="取得單一角色詳情",
    description="根據角色ID取得單一角色詳細資訊。",
    responses={
        200: generic_success_response(
            RoleSerializer,
            method="Retrieve",
            example=[{
                "id": 1,
                "name": "Admin",
                "level": 1,
                "permissions": [
                    {"id": 1, "code": "orders:view", "description": "查看訂單"},
                    {"id": 2, "code": "orders:edit", "description": "編輯訂單"}
                ]
            }]
        ),
        404: OpenApiResponse(description="角色不存在"),
    }
)

role_update_schema = extend_schema(
    summary="更新角色",
    description="根據角色ID更新角色資訊，permissions提供ID列表。",
    request=RoleCreateUpdateSerializer,
    responses={
        200: generic_success_response(
            RoleSerializer,
            method="Update",
            example=[{
                "id": 2,
                "name": "Updated Staff",
                "level": 2,
                "permissions": [
                    {"id": 1, "code": "orders:view", "description": "查看訂單"},
                    {"id": 2, "code": "orders:edit", "description": "編輯訂單"}
                ]
            }]
        ),
        400: OpenApiResponse(description="請求格式錯誤"),
        404: OpenApiResponse(description="角色不存在"),
    },
)

role_delete_schema = extend_schema(
    summary="刪除角色",
    description="根據角色ID刪除角色。",
    responses={
        204: OpenApiResponse(description="角色刪除成功（無回傳內容）"),
        404: OpenApiResponse(description="角色不存在"),
    }
)
