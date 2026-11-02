from django.contrib import admin
from django.db.models import Count

from .models import Game, Genre, Studio, Tag, UserGame


class CatalogCountAdmin(admin.ModelAdmin):
    ordering = ("name", "pk")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(_game_count=Count("games", distinct=True))
        )

    @admin.display(description="Games", ordering="_game_count")
    def game_count(self, obj):
        return obj._game_count


@admin.register(Tag)
class TagAdmin(CatalogCountAdmin):
    list_display = ("name", "slug", "game_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(CatalogCountAdmin):
    list_display = ("name", "slug", "game_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Studio)
class StudioAdmin(CatalogCountAdmin):
    list_display = ("name", "game_count")
    search_fields = ("name",)


class UserGameInline(admin.TabularInline):
    model = UserGame
    fields = ("user", "list_type", "play_status", "rating")
    autocomplete_fields = ("user",)
    extra = 0
    show_change_link = True


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "studio", "release_date", "saved_by")
    list_editable = ("release_date",)
    search_fields = ("title", "studio__name", "seed_key")
    list_filter = ("studio", "genres", "tags", "release_date")
    filter_horizontal = ("genres", "tags")
    list_select_related = ("studio",)
    ordering = ("title", "pk")
    autocomplete_fields = ("studio",)
    readonly_fields = ("seed_key", "saved_by")
    inlines = (UserGameInline,)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(_saved_by=Count("library_entries", distinct=True))
        )

    @admin.display(description="Saved by users", ordering="_saved_by")
    def saved_by(self, obj):
        return getattr(obj, "_saved_by", 0)


@admin.register(UserGame)
class UserGameAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "list_type", "play_status", "rating")
    list_editable = ("list_type", "play_status", "rating")
    list_filter = ("list_type", "play_status", "rating")
    search_fields = ("user__username", "game__title")
    autocomplete_fields = ("user", "game")
    list_select_related = ("user", "game")
    ordering = ("user__username", "game__title", "pk")
    fieldsets = (
        ("Collection", {"fields": ("user", "game", "list_type")}),
        ("Progress", {"fields": ("play_status", "rating")}),
        ("Private note", {"fields": ("note",)}),
    )


admin.site.site_header = "GameShelf administration"
admin.site.site_title = "GameShelf admin"
admin.site.index_title = "Manage catalog and collections"
