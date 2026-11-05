from rest_framework import generics, permissions, serializers

from .models import Game, Genre, Tag, UserGame
from .serializers import (
    GameSerializer,
    GenreSerializer,
    LibraryEntrySerializer,
    TagSerializer,
)
from .views import filtered_games


class PublicCatalog:
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()


class GameList(PublicCatalog, generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        games, form = filtered_games(self.request.query_params)
        if not form.is_valid():
            raise serializers.ValidationError(dict(form.errors))
        return games.prefetch_related("genres", "tags")


class GameDetail(PublicCatalog, generics.RetrieveAPIView):
    queryset = Game.objects.select_related("studio").prefetch_related(
        "genres", "tags"
    )
    serializer_class = GameSerializer


class GenreList(PublicCatalog, generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TagList(PublicCatalog, generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CurrentUserLibrary:
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LibraryEntrySerializer

    def get_queryset(self):
        return (
            UserGame.objects
            .filter(user=self.request.user)
            .select_related("game")
            .order_by("game__title", "pk")
        )


class LibraryList(CurrentUserLibrary, generics.ListAPIView):
    pass
