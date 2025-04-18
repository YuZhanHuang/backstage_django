from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.rbac.views.roles import RoleViewSet
from apps.rbac.views.permissions import PermissionViewSet

router = SimpleRouter(False)
router.register("roles", RoleViewSet)
router.register("permissions", PermissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
