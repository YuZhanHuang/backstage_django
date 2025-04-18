from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AvatarViewSet, UserViewSet

router = SimpleRouter(False)
router.register("", AvatarViewSet, basename="avatar")
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
