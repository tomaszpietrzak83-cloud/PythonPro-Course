from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # --- TASK 03 06 08 10 ---
    path("", include("myapp.urls")),
]
