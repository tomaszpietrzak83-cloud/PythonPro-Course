from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from myapp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("clients", views.ClientViewSet, basename="client")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", views.product_list, name="product_list"),
    path("api/task7/products-stats/", views.product_stats, name="product_stats"),
    path("api/task8/", include(router.urls)),
]

if settings.DEBUG_TOOLBAR_INSTALLED:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
