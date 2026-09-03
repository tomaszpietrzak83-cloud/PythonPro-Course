from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "short_description"]
    search_fields = ["name", "short_description"]

# Register your models here.
