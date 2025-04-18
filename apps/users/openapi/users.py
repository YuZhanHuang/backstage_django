from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..serializers import (
    UserSerializer,
    UserCreateUpdateSerializer, UserActiveStatusSerializer
)
from utils.response import generic_success_response

user_list_schema = extend_schema(
    summary="取得使用者列表",
    description="取得後台使用者列表，支援透過帳號、暱稱、信箱等條件篩選。",
    parameters=[
        OpenApiParameter(name='username', description='帳號模糊搜尋', type=OpenApiTypes.STR),
        OpenApiParameter(name='roles', description='角色id，以逗號分隔 (例如 1,2)', type=OpenApiTypes.STR),
        OpenApiParameter(name='is_active', description='啟用狀態', type=OpenApiTypes.BOOL),
    ],
    responses={
        200: generic_success_response(
            UserSerializer,
            method="List",
            example=[{
                "id": 1,
                "username": "user123",
                "nickname": "Mike",
                "email": "mike@example.com",
                "phone": "0912345678",
                "is_active": True,
                "roles": [
                    {"id": 1, "name": "Manager", "level": 2, "permissions": []}
                ],
            }]
        )
    }
)

user_create_schema = extend_schema(
    summary="建立新使用者",
    description="新增一個新的後台使用者。",
    request=UserCreateUpdateSerializer,
    responses={
        201: generic_success_response(
            UserSerializer,
            method="Create",
            example=[{
                "id": 1,
                "username": "user123",
                "nickname": "Mike",
                "email": "mike@example.com",
                "phone": "0912345678",
                "roles": [
                    2, 3
                ],
            }]
        )
    },
)

user_update_schema = extend_schema(
    summary="更新使用者資訊",
    description="更新使用者的資訊，僅更新指定欄位即可。",
    request=UserCreateUpdateSerializer,
    responses={
        200: generic_success_response(
            UserSerializer,
            method="Update",
            example=[{
                "id": 1,
                "username": "user123",
                "nickname": "Mike",
                "email": "mike@example.com",
                "phone": "0912345678",
                "is_active": True,
                "roles": [
                    {"id": 1, "name": "Manager", "level": 2, "permissions": []}
                ],
            }]
        ),
        400: OpenApiResponse(description="請求格式錯誤"),
        404: OpenApiResponse(description="使用者不存在"),
    }
)

user_retrieve_schema = extend_schema(
    summary="取得使用者詳情",
    description="根據使用者 ID 取得單一使用者詳細資料。",
    responses={
        200: generic_success_response(
            UserSerializer,
            method="Retrieve",
            example=[{
                "id": 1,
                "username": "user123",
                "nickname": "Mike",
                "email": "mike@example.com",
                "phone": "0912345678",
                "is_active": True,
                "roles": [
                    {"id": 1, "name": "Manager", "level": 2, "permissions": []}
                ],
            }]
        ),
        404: OpenApiResponse(description="使用者不存在"),
    }
)

user_delete_schema = extend_schema(
    summary="刪除使用者",
    description="根據使用者 ID 刪除特定使用者。",
    responses={
        204: OpenApiResponse(description="成功刪除使用者（無回傳內容）"),
        404: OpenApiResponse(description="使用者不存在"),
    }
)


user_set_active_status_schema = extend_schema(
    summary="設定使用者啟用狀態",
    description="根據使用者 ID 啟用或停用使用者。",
    request=UserActiveStatusSerializer,
    responses={
        200: OpenApiResponse(description="成功更新使用者啟用狀態", response=UserSerializer),
        400: OpenApiResponse(description="請求資料錯誤或驗證失敗"),
        404: OpenApiResponse(description="使用者不存在"),
        401: OpenApiResponse(description="未授權或身份驗證失敗"),
        403: OpenApiResponse(description="權限不足"),
    },
)
