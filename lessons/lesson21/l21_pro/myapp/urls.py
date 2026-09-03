from django.urls import path

from . import views

app_name = "myapp"

urlpatterns = [
    # --- TASK 03 ---
    path("categories/", views.category_list_view, name="category_list"),
    # --- TASK 06 07 ---
    path(
        "categories/<int:pk>/",
        views.category_detail_view,
        name="category_detail",
    ),
    # --- TASK 08 10 ---
    path("articles/", views.article_list_view, name="article_list"),
]
