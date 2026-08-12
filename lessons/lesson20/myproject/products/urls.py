from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("info/", views.info, name="info"),
    path("rules/", views.rules, name="rules"),
    path("user/<str:username>/", views.user_greeting, name="user_greeting"),
    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_creation, name="product_creation"),
    path(
        "category/<int:category_id>/", views.category_view, name="category_view"
    ),
]
