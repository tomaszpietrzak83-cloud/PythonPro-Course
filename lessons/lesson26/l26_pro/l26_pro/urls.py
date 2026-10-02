from django.contrib import admin
from django.urls import include, path
from myapp.views import (
    AdminInfoView,
    AdminStatsView,
    CustomTokenObtainPairView,
    RequestIdView,
    SomeProtectedView,
    StatusView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # TASK 04
    path("auth/", include("djoser.urls")),
    # TASK 04
    path("auth/", include("djoser.urls.jwt")),
    # TASK 08
    path("user/", SomeProtectedView.as_view()),
    # TASK 18
    path("api/admin-info/", AdminInfoView.as_view()),
    # TASK 22
    path("api/request-id/", RequestIdView.as_view()),
    # TASK 25
    path("api/status/", StatusView.as_view()),
    # TASK 25
    path("api/admin-stats/", AdminStatsView.as_view()),
    # TASK 24
    path("auth/jwt/custom-create/", CustomTokenObtainPairView.as_view()),
    # TASK 25
    path("api/", include("notes.urls")),
]
