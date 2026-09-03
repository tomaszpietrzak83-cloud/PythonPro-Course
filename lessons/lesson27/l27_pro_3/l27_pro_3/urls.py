from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from myapp3 import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products-viewset", views.ProductViewSet, basename="product")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/task10/", include("myapp3.urls")),
    path("api/task10/", include(router.urls)),
]

if settings.DEBUG_TOOLBAR_INSTALLED:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
