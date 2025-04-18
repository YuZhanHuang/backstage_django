import re
import phonenumbers
from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email(value):
    """
    驗證 Email 格式
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, value):
        raise ValidationError("請輸入有效的電子郵件地址")
    return value


def validate_phone(value):
    """
    驗證全世界手機格式，使用 `phonenumbers` 套件
    """
    try:
        parsed_number = phonenumbers.parse(value, None)  # 自動解析國家碼
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError("請輸入有效的手機號碼")
    except phonenumbers.NumberParseException:
        raise ValidationError("請輸入有效的手機號碼")

    return value


def validate_image_format(image):
    """使用 Pillow 驗證圖片格式"""
    try:
        img = Image.open(image)
        # TODO: 未來可接受的格式可能會擴充
        valid_formats = ["JPEG", "PNG", "GIF", "WEBP"]
        print('valid_formats', img.format, flush=True)
        if img.format not in valid_formats:
            raise ValidationError("僅支援 JPG、PNG、GIF 格式的圖片。")

    except Exception:
        raise ValidationError("無法解析圖片格式，請確保上傳正確的圖片檔案。")

    return image


def validate_password_complexity(
        password,
        min_length=8,
        max_length=20,
        require_upper=True,
        require_lower=True,
        require_digit=True,
        require_special=True,
        special_chars="._-",
        forbid_spaces=True,
        forbid_fullwidth=True
):
    """
    驗證密碼的強度，提供可調整的規則。

    :param password: 使用者輸入的密碼
    :param min_length: 最小長度
    :param max_length: 最大長度
    :param require_upper: 是否要求至少一個大寫字母
    :param require_lower: 是否要求至少一個小寫字母
    :param require_digit: 是否要求至少一個數字
    :param require_special: 是否要求至少一個特殊字元
    :param special_chars: 允許的特殊字元字串
    :param forbid_spaces: 是否禁止空格
    :param forbid_fullwidth: 是否禁止全形字元
    :raises ValidationError: 當密碼不符合條件時拋出錯誤
    """

    # 1. 密碼不能為空
    if not password:
        raise ValidationError(_("密碼不能為空"))

    # 2. 禁用空格（根據 `forbid_spaces`）
    if forbid_spaces and any(char.isspace() for char in password):
        raise ValidationError(_("密碼不能包含空格"))

    # 3. 禁用全形字元（根據 `forbid_fullwidth`）
    if forbid_fullwidth and re.search(r"[Ａ-Ｚａ-ｚ０-９＿－．]", password):
        raise ValidationError(_("密碼不能包含全形字元"))

    # 4. 檢查密碼是否符合強度要求
    if require_lower and not re.search(r"[a-z]", password):
        raise ValidationError(_("密碼必須包含至少一個小寫字母"))
    if require_upper and not re.search(r"[A-Z]", password):
        raise ValidationError(_("密碼必須包含至少一個大寫字母"))
    if require_digit and not re.search(r"\d", password):
        raise ValidationError(_("密碼必須包含至少一個數字"))
    if require_special and not any(char in special_chars for char in password):
        raise ValidationError(_("密碼必須包含至少一個特殊字元（{}）").format(special_chars))

    # 5. 確保密碼長度
    if not (min_length <= len(password) <= max_length):
        raise ValidationError(_("密碼長度必須介於 {} 到 {} 個字元之間").format(min_length, max_length))


def validate_username(username, min_length=6, max_length=20, allowed_special="._-"):
    if not username:
        raise ValidationError("帳號不能為空")

    if any(char.isspace() for char in username):
        raise ValidationError("帳號不能包含空格")

    if any('\uFF01' <= char <= '\uFF5E' for char in username):
        raise ValidationError("帳號不能包含全形字元")

    if not re.match(rf'^[A-Za-z0-9{re.escape(allowed_special)}]+$', username):
        raise ValidationError(f"帳號只能包含英文字母、數字以及特殊字元 ({allowed_special})")

    if not (min_length <= len(username) <= max_length):
        raise ValidationError(f"帳號長度必須介於 {min_length} 到 {max_length} 個字元之間")


def custom_password_validation(password, allowed_special_chars="._-"):
    if not password:
        raise ValidationError(_("密碼不能為空"))

    if any(char.isspace() for char in password):
        raise ValidationError(_("密碼不能包含空格"))

    if re.search(r"[Ａ-Ｚａ-ｚ０-９＿－．]", password):
        raise ValidationError(_("密碼不能包含全形字元"))

    if any(not char.isalnum() and char not in allowed_special_chars for char in password):
        raise ValidationError(_("密碼只能包含英數字和這些特殊字元 ({})").format(allowed_special_chars))