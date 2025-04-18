from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginViewSet, LogoutViewSet, ResetPasswordViewSet

router = SimpleRouter(False)
router.register("", ResetPasswordViewSet, basename="reset_password")
router.register("", LogoutViewSet, basename="logout")


urlpatterns = [
    path("", include(router.urls)),
    # JWT 登入/登出
    path("login/", LoginViewSet.as_view(), name="custom_auth-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="custom_auth-token-refresh"),
]
