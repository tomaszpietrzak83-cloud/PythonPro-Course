from rest_framework import generics, permissions, serializers
from drf_spectacular.utils import extend_schema, extend_schema_view

from .api_schema import CATALOG_PARAMETERS, FORBIDDEN, INVALID_FILTER, NOT_FOUND
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


@extend_schema_view(get=extend_schema(
    tags=["Catalog"], summary="List games", parameters=CATALOG_PARAMETERS,
    description="Combine title, genre and tag filters. Use genre=fake and tag=fake for seeded games.",
    responses={200: GameSerializer(many=True), 400: INVALID_FILTER},
))
class GameList(PublicCatalog, generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        games, form = filtered_games(self.request.query_params)
        if not form.is_valid():
            raise serializers.ValidationError(dict(form.errors))
        return games.prefetch_related("genres", "tags")


@extend_schema_view(get=extend_schema(
    tags=["Catalog"], summary="Get a game", responses={200: GameSerializer, 404: NOT_FOUND},
))
class GameDetail(PublicCatalog, generics.RetrieveAPIView):
    queryset = Game.objects.select_related("studio").prefetch_related(
        "genres", "tags"
    )
    serializer_class = GameSerializer


@extend_schema_view(get=extend_schema(tags=["Catalog"], summary="List genres"))
class GenreList(PublicCatalog, generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@extend_schema_view(get=extend_schema(tags=["Catalog"], summary="List tags"))
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


@extend_schema_view(get=extend_schema(
    tags=["My library"], summary="List my saved games",
    description="Uses your GameShelf session and returns only your own entries, including private notes.",
    responses={200: LibraryEntrySerializer(many=True), 403: FORBIDDEN},
))
class LibraryList(CurrentUserLibrary, generics.ListAPIView):
    pass
