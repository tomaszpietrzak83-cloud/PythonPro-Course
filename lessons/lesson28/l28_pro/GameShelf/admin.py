from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date")
    search_fields = ("title",)
    list_filter = ("release_date",)
