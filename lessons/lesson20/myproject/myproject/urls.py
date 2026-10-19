from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
    path("", include("notes.urls")),
]
