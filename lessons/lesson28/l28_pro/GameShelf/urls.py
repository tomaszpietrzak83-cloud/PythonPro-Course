from django.urls import path

from . import views

app_name = "gameshelf"

urlpatterns = [
    path("", views.home, name="home"),
    path("games/", views.game_list, name="game_list"),
]
