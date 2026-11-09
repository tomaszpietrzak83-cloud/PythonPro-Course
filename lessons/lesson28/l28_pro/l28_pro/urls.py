from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(
            url_name="api-schema", template_name="gameshelf_swagger.html"
        ),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="redoc",
    ),
    path("api/v1/", include("GameShelf.api_urls")),
    path("", include("GameShelf.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
