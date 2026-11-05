from rest_framework import serializers

from .models import Game, Genre, Tag, UserGame


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "slug")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class GameSerializer(serializers.ModelSerializer):
    studio = serializers.CharField(source="studio.name", allow_null=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_url = serializers.SerializerMethodField()

    def get_cover_url(self, game) -> str:
        return self.context["request"].build_absolute_uri(game.cover_url)

    class Meta:
        model = Game
        fields = ("id", "title", "description", "release_date", "studio", "genres", "tags", "cover_url")


class LibraryEntrySerializer(serializers.ModelSerializer):
    game_title = serializers.CharField(source="game.title", read_only=True)

    class Meta:
        model = UserGame
        fields = ("id", "game", "game_title", "list_type", "play_status", "rating", "note")
        read_only_fields = fields
