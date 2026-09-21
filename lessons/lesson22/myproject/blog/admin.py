from django.contrib import admin

from .models import Author, Category, Post, PostTag, Tag


class PostTagInline(admin.TabularInline):
    model = PostTag
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "publication_date")
    list_filter = ("category", "tags", "publication_date")
    search_fields = ("title", "content", "author__first_name", "author__last_name")
    inlines = [PostTagInline]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
