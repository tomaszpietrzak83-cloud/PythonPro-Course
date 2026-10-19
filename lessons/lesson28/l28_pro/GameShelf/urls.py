from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "gameshelf"

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("games/", views.game_list, name="game_list"),
    path("games/suggestions/", views.game_suggestions, name="game_suggestions"),
    path("games/<int:pk>/", views.game_detail, name="game_detail"),
]
