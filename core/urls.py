from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf.urls.static import static
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from core import settings


api_urlpatterns = [
    # Swagger API 文檔
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Apps
    path("users/", include("apps.users.urls")),
    path("rbac/", include("apps.rbac.urls")),
    path("auth/", include("apps.custom_auth.urls")),
    path("health/", include("apps.health.urls")),
]


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("docs"))),
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_urlpatterns)),  # 註冊當前 API
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
