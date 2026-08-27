from django.contrib import admin
from django.urls import include, path
from new_app import views
from rest_framework import routers

router = routers.DefaultRouter()
# TASK 03
router.register(r"products", views.ProductViewSet)

# TASK 06
router.register(r"notes", views.NoteViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # TASK 05
    path("api/set-name/", views.set_name),
    # TASK 05
    path("api/hello/", views.hello),
    # TASK 07
    path("api/calculate/", views.calculate),
]
