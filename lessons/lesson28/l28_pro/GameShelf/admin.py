from django.contrib import admin

from .models import Game, Genre, Studio, Tag, UserGame


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "studio", "release_date")
    search_fields = ("title", "studio__name")
    list_filter = ("studio", "genres", "tags", "release_date")
    filter_horizontal = ("genres", "tags")
    list_select_related = ("studio",)


@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "list_type")
    list_filter = ("list_type",)
    search_fields = ("user__username", "game__title")
    autocomplete_fields = ("user", "game")
    list_select_related = ("user", "game")
