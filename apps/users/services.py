from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


def update_user_bindings(user, validated_data):
    """
    更新使用者的綁定資料，並根據變更調整驗證狀態
    """
    is_updated = False

    phone = validated_data.get("phone", "")
    email = validated_data.get("email", "")
    nickname = validated_data.get("nickname", "")

    phone_validated = cache.get(f"temp_user_phone-{phone}", {}).get('is_verified') is True
    email_validated = cache.get(f"temp_user_email-{email}", {}).get('is_verified') is True

    if "nickname" in validated_data and validated_data["nickname"] != user.nickname:
        user.nickname = nickname
        is_updated = True

    # 取得緩存確認email是否驗證成功
    if "email" in validated_data and email_validated is True and email != user.email:
        user.email = email
        is_updated = True

    # 取得緩存確認phone是否驗證成功
    if "phone" in validated_data and phone_validated is True and phone != user.phone:
        user.phone = phone
        is_updated = True

    if is_updated:
        user.save()

    return user
