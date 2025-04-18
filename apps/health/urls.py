from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import HealthCheckViewSet

router = SimpleRouter(False)
router.register("", HealthCheckViewSet, basename="health")

urlpatterns = [
    path("", include(router.urls)),
]
