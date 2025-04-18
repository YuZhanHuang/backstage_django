from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField
from factory import Faker

from django.contrib.auth.hashers import make_password
from ..models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("user_name")
    email = LazyAttribute(lambda o: f"{o.username}@example.com")
    phone = Faker("numerify", text="09#########")  # ✅ 確保長度符合 15 個字以內
    nickname = Faker("user_name")  # 可以用 `user_name` 來模擬暱稱
    password = LazyAttribute(lambda o: make_password(o.username))  # 確保密碼被加密

    first_name = Faker("first_name")
    last_name = Faker("last_name")
    full_name = LazyAttribute(lambda o: f"{o.first_name} {o.last_name}")
    address = Faker("address")
    birthday = Faker("date_of_birth")
    avatar = ImageField(width=1000, height=1000)

    is_active = True
    is_staff = False
    is_email_verified = False
    is_phone_verified = False
