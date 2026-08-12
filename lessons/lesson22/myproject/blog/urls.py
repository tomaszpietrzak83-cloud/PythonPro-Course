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
]
