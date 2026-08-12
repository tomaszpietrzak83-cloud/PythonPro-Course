from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from my_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # TASK 02 03 05 06 10
    path("", include("my_app.urls")),
    # TASK 07
    path(
        "login/",
        views.CustomLoginView.as_view(),
        name="login",
    ),
    # TASK 02
    path(
        "logout/",
        views.CustomLogoutView.as_view(),
        name="logout",
    ),
    # TASK 08
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change_form.html"
        ),
        name="password_change",
    ),
    # TASK 08
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
