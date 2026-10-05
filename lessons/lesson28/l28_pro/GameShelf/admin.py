from django.contrib import admin

from .models import Game, Genre, Studio


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
    list_filter = ("studio", "genres", "release_date")
    filter_horizontal = ("genres",)
    list_select_related = ("studio",)
