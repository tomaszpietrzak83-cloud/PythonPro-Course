from django.contrib import admin
from django.utils.html import format_html

from .models import Car, Dealer


# TASK 10
class CarInline(admin.TabularInline):
    model = Car
    extra = 1


# TASK 10
@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    inlines = [CarInline]


# TASK 01 02 03 04 05 06 07 08 09
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # TASK 02 06 09
    list_display = ("full_name", "year", "is_available", "display_photo")
    # TASK 03
    search_fields = ("brand", "model")
    # TASK 04
    list_filter = ("is_available", "year")
    # TASK 05
    ordering = ("-year",)
    # TASK 07
    readonly_fields = ("year",)
    # TASK 08
    actions = ("mark_as_unavailable", "mark_as_available")

    # TASK 06
    def full_name(self, obj):
        return f"{obj.brand} {obj.model}"

    # TASK 06
    full_name.short_description = "Full Name"

    # TASK 08
    def mark_as_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        self.message_user(
            request, "Selected cars have been marked as unavailable."
        )

    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
        self.message_user(
            request, "Selected cars have been marked as available."
        )

    # TASK 09
    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="150" />', obj.photo.url)
        return "No photo available"

    # TASK 09
    display_photo.short_description = "Photo"
