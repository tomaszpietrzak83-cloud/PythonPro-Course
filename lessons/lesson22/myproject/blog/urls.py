from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # TASK 03 06
    path("", views.post_views, name="post_views"),
    # TASK 02
    path(
        "category/<int:category_id>/", views.category, name="sort_by_category"
    ),
    # SEARCH-SITE
    path("articles/search/", views.article_search, name="article_search"),
    path("articles/search/help/", views.search_help, name="search_help"),
    path(
        "articles/search/authors/",
        views.author_suggestions,
        name="author_suggestions",
    ),
    path(
        "articles/search/tags/", views.tag_suggestions, name="tag_suggestions"
    ),
    path("articles/<int:post_id>/", views.article_detail, name="article_detail"),
]
