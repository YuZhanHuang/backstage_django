from rest_framework.exceptions import APIException, AuthenticationFailed


class CustomAPIException(APIException):
    """自訂 API 例外處理，提供統一格式"""

    status_code = 400  # 預設 HTTP 狀態碼
    default_detail = "發生未知錯誤"  # 預設錯誤訊息
    default_code = "error"  # 預設錯誤碼

    def __init__(self, detail=None, status_code=None):
        """
        :param detail: 錯誤訊息，可選
        :param status_code: HTTP 狀態碼，可選
        """
        if detail is None:
            detail = self.default_detail
        self.detail = {"success": False, "message": detail}

        if status_code is not None:
            self.status_code = status_code


class ValidationException(CustomAPIException):
    status_code = 422
    default_detail = "請求參數驗證失敗"


class PermissionDeniedException(CustomAPIException):
    status_code = 403
    default_detail = "權限不足"


class NotFoundException(CustomAPIException):
    status_code = 404
    default_detail = "資源未找到"


class ServerErrorException(CustomAPIException):
    status_code = 500
    default_detail = "內部伺服器錯誤"


class AccountLocked(AuthenticationFailed):
    status_code = 403
    default_detail = "帳號已被暫時鎖定 5 分鐘，請稍後再試。"


class AccountDisabled(AuthenticationFailed):
    status_code = 403
    default_detail = "帳號已被凍結，請聯絡客服處理。"


class InvalidCredentials(AuthenticationFailed):
    status_code = 401
    default_detail = "登入失敗，請確認帳號或密碼。"
