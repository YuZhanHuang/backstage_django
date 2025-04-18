import traceback

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from structlog import get_logger

from .exceptions import CustomAPIException

logger = get_logger(__name__)


def custom_exception_handler(exc, context):
    """
    自訂全域異常處理，確保所有錯誤統一格式，並使用 `structlog` 記錄錯誤資訊
    """
    request = context.get("request", None)
    error_stack = traceback.format_exc()

    # 預設錯誤訊息
    error_type = type(exc).__name__
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR  # 預設 HTTP 狀態碼
    error_messages = []

    # 使用 DRF 預設的異常處理
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        # 確保錯誤訊息是字串
        status_code = exc.status_code
        error_messages.append(str(exc.detail))

    elif response is not None:
        status_code = response.status_code
        if isinstance(response.data, dict):
            for field, messages in response.data.items():
                if isinstance(messages, list):
                    for msg in messages:
                        translated_msg = str(_(msg)) if isinstance(msg, str) else str(msg)
                        if translated_msg == msg:
                            logger.info(f"未翻譯的錯誤訊息: {msg}")
                        error_messages.append(f"{field}: {translated_msg}")

                elif isinstance(messages, str):
                    translated_msg = str(_(messages))
                    if translated_msg == messages:
                        logger.info(f"未翻譯的錯誤訊息: {messages}")
                    error_messages.append(f"{field}: {translated_msg}")

                elif isinstance(messages, dict):  # 處理 JWT Token 類錯誤
                    for sub_field, sub_messages in messages.items():
                        sub_error_list = [str(_(msg)) if isinstance(msg, str) else str(msg) for msg in sub_messages]
                        error_messages.append(f"{field} - {sub_field}: {'；'.join(sub_error_list)}")

        else:
            error_messages.append(str(response.data))

    else:
        error_messages.append(str(exc))

    # 最終組合錯誤訊息
    error_message = "；".join(error_messages) if error_messages else "發生未知錯誤"

    # 記錄錯誤日誌
    logger.error(
        "API 發生錯誤",
        error_type=error_type,
        error_message=error_message,
        status_code=status_code,
        request_path=request.path if request else "N/A",
        request_method=request.method if request else "N/A",
        user=str(request.user) if request and request.user.is_authenticated else "Anonymous",
        stack_trace=error_stack,
    )

    # 返回統一格式的錯誤響應
    return Response({"success": False, "message": error_message}, status=status_code)



