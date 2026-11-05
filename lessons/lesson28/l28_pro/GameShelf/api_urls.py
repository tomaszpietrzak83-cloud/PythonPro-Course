from django.urls import path

from . import api

app_name = "gameshelf_api"

urlpatterns = [
    path("games/", api.GameList.as_view(), name="game-list"),
    path("games/<int:pk>/", api.GameDetail.as_view(), name="game-detail"),
    path("genres/", api.GenreList.as_view(), name="genre-list"),
    path("tags/", api.TagList.as_view(), name="tag-list"),
    path("library/", api.LibraryList.as_view(), name="library-list"),
]
