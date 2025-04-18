from allauth.account.adapter import DefaultAccountAdapter
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    """自訂帳號 Adapter，適用於一般帳號行為"""

    def save_user(self, request, user, form, commit=True):
        """
        在一般帳號建立時，確保 `nickname` 唯一
        """
        user = super().save_user(request, user, form, commit=False)

        if not user.nickname:
            user.nickname = self.generate_unique_nickname("user")

        user.nickname = self.generate_unique_nickname(user.nickname)

        if commit:
            user.save()
        return user

    def generate_unique_nickname(self, base_nickname):
        """確保 `nickname` 唯一，避免 `IntegrityError`"""
        nickname = slugify(base_nickname)
        if not nickname:
            nickname = f"user-{uuid.uuid4().hex[:8]}"

        unique_nickname = nickname
        counter = 1

        while User.objects.filter(nickname=unique_nickname).exists():
            unique_nickname = f"{nickname}-{counter}"
            counter += 1
            if len(unique_nickname) > 50:
                unique_nickname = f"user-{uuid.uuid4().hex[:8]}"
        return unique_nickname
