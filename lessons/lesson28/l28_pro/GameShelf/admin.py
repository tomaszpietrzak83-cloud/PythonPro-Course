from django.contrib import admin

from .models import Game, Studio


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "studio", "release_date")
    search_fields = ("title", "studio__name")
    list_filter = ("studio", "release_date")
    list_select_related = ("studio",)
