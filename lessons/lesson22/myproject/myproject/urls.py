from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # TASK 02 03 06
    path("", include("blog.urls")),
    # TASK 10
    path("accounts/", include("allauth.urls")),
]
