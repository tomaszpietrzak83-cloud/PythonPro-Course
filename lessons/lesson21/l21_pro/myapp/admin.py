from django.contrib import admin

from .models import Article, Category


# --- TASK 01 07 08 09 ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# --- TASK 07 08 10 ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "pub_date")
    list_filter = ("category", "is_published")
    search_fields = ("title", "content")


# --- TASK 09 ---
admin.site.site_header = "My Site Administrator Panel"
admin.site.site_title = "My Site Administrator Panel"
admin.site.index_title = "My Site Administrator Panel"
