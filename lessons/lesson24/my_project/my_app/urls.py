from django.urls import path

from . import views

urlpatterns = [
    # TASK 05
    path("", views.home, name="home"),
    # TASK 06 09
    path("register/", views.register, name="register"),
    # TASK 03
    path("profile/", views.profile, name="profile"),
    # TASK 10
    path("user_list/", views.user_list, name="user_list"),
]
