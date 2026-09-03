from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/task6/", include("myapp2.urls")),
]

if settings.DEBUG_TOOLBAR_INSTALLED:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
