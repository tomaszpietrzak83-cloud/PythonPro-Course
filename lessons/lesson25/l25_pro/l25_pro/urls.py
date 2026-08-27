from django.contrib import admin
from django.urls import include, path
from new_app import views
from rest_framework import routers

router = routers.DefaultRouter()
# TASK 03
router.register(r"products", views.ProductViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
