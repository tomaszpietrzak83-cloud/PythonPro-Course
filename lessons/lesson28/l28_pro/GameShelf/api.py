from django.db import transaction
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from .api_schema import (
    CATALOG_PARAMETERS,
    FORBIDDEN,
    INVALID_ENTRY,
    INVALID_FILTER,
    NOT_FOUND,
)
from .models import Game, Genre, Tag, UserGame
from .serializers import (
    GameSerializer,
    GenreSerializer,
    LibraryCreateSerializer,
    LibraryEntrySerializer,
    LibraryUpdateSerializer,
    TagSerializer,
)
from .views import filtered_games


class PublicCatalog:
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()


@extend_schema_view(
    get=extend_schema(
        tags=["Catalog"],
        summary="List games",
        parameters=CATALOG_PARAMETERS,
        description="Combine title, genre and tag filters. Use genre=fake and tag=fake for seeded games.",
        responses={200: GameSerializer(many=True), 400: INVALID_FILTER},
    )
)
class GameList(PublicCatalog, generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        games, form = filtered_games(self.request.query_params)
        if not form.is_valid():
            raise serializers.ValidationError(dict(form.errors))
        return games.prefetch_related("genres", "tags")


@extend_schema_view(
    get=extend_schema(
        tags=["Catalog"],
        summary="Get a game",
        responses={200: GameSerializer, 404: NOT_FOUND},
    )
)
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
    queryset = UserGame.objects.none()

    def get_queryset(self):
        return (
            UserGame.objects
            .filter(user=self.request.user)
            .select_related("game")
            .order_by("game__title", "pk")
        )


@extend_schema_view(
    get=extend_schema(
        tags=["My library"],
        summary="List my saved games",
        description="Uses your GameShelf session and returns only your own entries, including private notes.",
        responses={200: LibraryEntrySerializer(many=True), 403: FORBIDDEN},
    )
)
class LibraryList(CurrentUserLibrary, generics.ListCreateAPIView):
    @extend_schema(
        tags=["My library"],
        summary="Save a game",
        description="Send a game ID from the catalog and a list type. Duplicate games return 400.",
        request=LibraryCreateSerializer,
        responses={
            201: LibraryEntrySerializer,
            400: INVALID_ENTRY,
            403: FORBIDDEN,
        },
        examples=[
            OpenApiExample(
                "Add to wishlist",
                value={"game": 1, "list_type": "wishlist"},
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = LibraryCreateSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        entry = serializer.save()
        return Response(
            self.get_serializer(entry).data, status=status.HTTP_201_CREATED
        )


@extend_schema_view(
    get=extend_schema(
        tags=["My library"],
        summary="Get my saved game",
        responses={200: LibraryEntrySerializer, 403: FORBIDDEN, 404: NOT_FOUND},
    ),
    delete=extend_schema(
        tags=["My library"],
        summary="Remove my saved game",
        description="Removes the library entry, not the public game.",
        responses={204: None, 403: FORBIDDEN, 404: NOT_FOUND},
    ),
)
class LibraryDetail(CurrentUserLibrary, generics.RetrieveDestroyAPIView):
    def get_queryset(self):
        entries = super().get_queryset()
        if self.request.method == "PATCH":
            return entries.select_for_update(of=("self",))
        return entries

    @extend_schema(
        tags=["My library"],
        summary="Update my saved game",
        description="Ratings are 1–10 or null. You can move wishlist to owned, but not owned to wishlist.",
        request=LibraryUpdateSerializer(partial=True),
        responses={
            200: LibraryEntrySerializer,
            400: INVALID_ENTRY,
            403: FORBIDDEN,
            404: NOT_FOUND,
        },
        examples=[
            OpenApiExample(
                "Move to owned", value={"list_type": "owned"}, request_only=True
            ),
            OpenApiExample(
                "Rate a completed game",
                value={"play_status": "completed", "rating": 9},
                request_only=True,
            ),
            OpenApiExample(
                "Rating outside range",
                value={
                    "rating": ["Ensure this value is less than or equal to 10."]
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    )
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        entry = self.get_object()
        serializer = LibraryUpdateSerializer(
            entry, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(self.get_serializer(serializer.save()).data)
