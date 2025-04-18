import re

from django.core.exceptions import ValidationError


def validate_taiwan_phone(value):
    if not re.match(r"^09\d{8}$", value):
        raise ValidationError("手機號碼格式錯誤，需符合台灣手機號碼格式 09XXXXXXXX")


def validate_email(value):
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        raise ValidationError("Email 格式錯誤")
