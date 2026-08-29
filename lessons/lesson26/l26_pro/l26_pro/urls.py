from django.contrib import admin
from django.urls import include, path
from myapp.views import SomeProtectedView

urlpatterns = [
    path("admin/", admin.site.urls),
    # TASK 04
    path("auth/", include("djoser.urls")),
    # TASK 04
    path("auth/", include("djoser.urls.jwt")),
    # TASK 08
    path("user/", SomeProtectedView.as_view()),
]
